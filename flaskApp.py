from flask import Flask, render_template, request
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__, static_url_path='/static')

xss_payloads_file = 'xss-payload-list.txt'
sqli_payloads_file = 'randon.txt'

with open(sqli_payloads_file, 'r', encoding='utf-8') as file:
    sqli_payloads = file.readlines()

with open(xss_payloads_file, 'r', encoding='utf-8') as file:
    xss_payloads = file.readlines()


def make_request_with_rate_limit(session, url, payload=None):
    try:
        if payload:
            url = f"{url}?parameter={payload.strip()}"
        response = session.get(url, verify=True, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None


def scan_sql_injection(url, payload, session, results):
    response = make_request_with_rate_limit(session, url, payload)
    if response and ('error' in response.text.lower() or 'exception' in response.text.lower()):
        results.append(f'Vulnerability Found: SQL Injection Detected with Payload "{payload.strip()}"')


def scan_xss_payload(url, payload, session, results):
    response = make_request_with_rate_limit(session, url)
    if response and payload.strip() in response.text:
        results.append(f'Vulnerability Found: XSS Payload "{payload.strip()}" Detected')


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        url = request.form.get('urlInput')

        if not url:
            return render_template('scan.html', error='URL is required. Please enter a URL.')

        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        results = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures_sqli = [executor.submit(scan_sql_injection, url, payload, session, results) for payload in sqli_payloads]
            futures_xss = [executor.submit(scan_xss_payload, url, payload, session, results) for payload in xss_payloads]

            for _ in as_completed(futures_sqli):
                pass

            response = make_request_with_rate_limit(session, url)

            if response:
                if 'X-Content-Type-Options' not in response.headers:
                    results.append('Vulnerability Found: X-Content-Type-Options Header Missing')

                if 'X-Frame-Options' not in response.headers:
                    results.append('Vulnerability Found: X-Frame-Options Setting Malformed')

                if 'X-Powered-By' in response.headers:
                    results.append(f'Vulnerability Found: Server Leaks Information via "X-Powered-By" - {response.headers["X-Powered-By"]}')

            for _ in as_completed(futures_xss):
                pass

            session.close()

        return render_template('scan.html', success='Scan completed successfully.', url=url, results=results)

    return render_template('scan.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
