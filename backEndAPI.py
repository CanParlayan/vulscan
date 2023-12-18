from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/report_vulnerability', methods=['POST'])
def report_vulnerability():
    data = request.get_json()

    # Simulate storing the vulnerability report in a database
    # Replace this with your actual database storage logic
    # Example: database.store_vulnerability(data)

    print(f"Received vulnerability report: {data}")

    return jsonify({"message": "Vulnerability reported successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
