from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='api_log_lateset.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


@app.route('/log_data', methods=['POST'])
def log_data():
    data = request.json
    headers = request.headers
    logging.info(f"Data received: {data}")
    logging.info(f"Headers received: {headers}")

    challenge = data.get('challenge')
    if challenge:
        print("Responding with challenge")
        return challenge, 200, {'Content-Type': 'text/plain'}
    else:
        print("Processing event data")
        # Respond to Slack event
        return 'Event received', 200


if __name__ == '__main__':
    app.run(debug=True)
