from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/report_vulnerability', methods=['POST'])
def report_vulnerability():
    data = request.get_json()

    # Simulate processing the vulnerability report on the frontend
    # Replace this with your actual logic for handling vulnerability reports
    # Example: frontend.process_vulnerability_report(data)

    print(f"Received vulnerability report on frontend: {data}")

    return jsonify({"message": "Vulnerability reported successfully on frontend"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
