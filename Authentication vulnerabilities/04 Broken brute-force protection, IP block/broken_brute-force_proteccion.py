"""
This script is designed to automate the process of testing for broken brute-force protection
 vulnerabilities in web applications based in the PortSwigger Labs "
 Authentication vulnerabilities" series. It attempts to brute-force login 
 credentials while monitoring for any signs of broken protection mechanisms, 
 such as lack of account lockout or IP blocking."""

import requests
