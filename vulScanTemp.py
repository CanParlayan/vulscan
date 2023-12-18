from urllib3.exceptions import InsecureRequestWarning
import requests
from tqdm import tqdm
import time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Functions for fetching data from database and making API calls

def get_sql_injection_payloads_from_db():
    return ["payload1", "payload2", "payload3"]

def get_xss_payloads_from_db():
    return ["xss_payload1", "xss_payload2", "xss_payload3"]

def report_vulnerability_to_backend(vulnerability_info):
    backend_api_url = "https://backend-api/report_vulnerability"
    response = requests.post(backend_api_url, json=vulnerability_info)
    # Handle the response as needed

def report_vulnerability_to_frontend(vulnerability_info):
    frontend_api_url = "https://frontend-api/report_vulnerability"
    response = requests.post(frontend_api_url, json=vulnerability_info)
    # Handle the response as needed

def scan_website(url):
    response = requests.get(url, verify=False)

    sqli_payloads = get_sql_injection_payloads_from_db()
    xss_payloads = get_xss_payloads_from_db()

    for payload in tqdm(sqli_payloads, desc='Scanning SQL Injection'):
        inject_url = f"{url}?parameter={payload}"
        response = requests.get(inject_url, verify=False)

        if 'error' in response.text.lower() or 'exception' in response.text.lower():
            print(f'Vulnerability Found: SQL Injection Detected with Payload "{payload}"')
            vulnerability_info = {"vulnerability_type": "SQL Injection", "payload": payload}
            report_vulnerability_to_backend(vulnerability_info)
            report_vulnerability_to_frontend(vulnerability_info)

    if 'X-Content-Type-Options' not in response.headers:
        print('Vulnerability Found: X-Content-Type-Options Header Missing')
        vulnerability_info = {"vulnerability_type": "X-Content-Type-Options Header Missing"}
        report_vulnerability_to_backend(vulnerability_info)
        report_vulnerability_to_frontend(vulnerability_info)

    if 'X-Frame-Options' not in response.headers:
        print('Vulnerability Found: X-Frame-Options Setting Malformed')
        vulnerability_info = {"vulnerability_type": "X-Frame-Options Setting Malformed"}
        report_vulnerability_to_backend(vulnerability_info)
        report_vulnerability_to_frontend(vulnerability_info)

    if 'X-Powered-By' in response.headers:
        print(f'Vulnerability Found: Server Leaks Information via "X-Powered-By" - {response.headers["X-Powered-By"]}')
        vulnerability_info = {"vulnerability_type": "Server Information Leakage", "info": response.headers["X-Powered-By"]}
        report_vulnerability_to_backend(vulnerability_info)
        report_vulnerability_to_frontend(vulnerability_info)

    for payload in tqdm(xss_payloads, desc='Scanning XSS Payloads'):
        if payload in response.text:
            print(f'Vulnerability Found: XSS Payload "{payload}" Detected')
            vulnerability_info = {"vulnerability_type": "XSS", "payload": payload}
            report_vulnerability_to_backend(vulnerability_info)
            report_vulnerability_to_frontend(vulnerability_info)

# Example usage
website_url = 'https://ebruparlayan.com'
scan_website(website_url)
