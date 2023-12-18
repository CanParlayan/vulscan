import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from time import sleep


def make_request_with_rate_limit(session, url, payload=None):
    try:
        if payload:
            url = f"{url}?parameter={payload.strip()}"
        response = session.get(url, verify=True, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None



def scan_sql_injection(url, payload, session):
    response = make_request_with_rate_limit(session, url, payload)
    if response and ('error' in response.text.lower() or 'exception' in response.text.lower()):
        print(f'Vulnerability Found: SQL Injection Detected with Payload "{payload.strip()}"')


def scan_xss_payload(url, payload, session):
    response = make_request_with_rate_limit(session, url)
    if response and payload.strip() in response.text:
        print(f'Vulnerability Found: XSS Payload "{payload.strip()}" Detected')


def scan_website(url, xss_payloads, sqli_payloads):
    # Create a Session with connection pooling and retry mechanism
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Use a list to store the futures
        futures = [executor.submit(scan_sql_injection, url, payload, session) for payload in sqli_payloads]

        # Use tqdm to visualize progress for SQL injection scans
        for future in tqdm(as_completed(futures), total=len(futures), desc='Scanning SQL Injection'):
            pass  # No need to do anything here, just iterating over futures

    response = make_request_with_rate_limit(session, url)

    if response:
        if 'X-Content-Type-Options' not in response.headers:
            print('Vulnerability Found: X-Content-Type-Options Header Missing')

        if 'X-Frame-Options' not in response.headers:
            print('Vulnerability Found: X-Frame-Options Setting Malformed')

        if 'X-Powered-By' in response.headers:
            print(
                f'Vulnerability Found: Server Leaks Information via "X-Powered-By" - {response.headers["X-Powered-By"]}')

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Use a list to store the futures
        futures = [executor.submit(scan_xss_payload, url, payload, session) for payload in xss_payloads]

        # Use tqdm to visualize progress for XSS scans
        for future in tqdm(as_completed(futures), total=len(futures), desc='Scanning XSS Payloads'):
            pass  # No need to do anything here, just iterating over futures

    # Close the session when done
    session.close()


website_url = 'https://drebruparlayan.com'
xss_payloads_file = 'xss-payload-list.txt'
sqli_payloads_file = 'randon.txt'

with open(sqli_payloads_file, 'r', encoding='utf-8') as file:
    sqli_payloads = file.readlines()

with open(xss_payloads_file, 'r', encoding='utf-8') as file:
    xss_payloads = file.readlines()

scan_website(website_url, xss_payloads, sqli_payloads)
