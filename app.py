import logging
import json
from flask import Flask, request
from cloudwatch_logger import logger  # Import CloudWatch logger
from jira_handler import create_jira_issue  # Import Jira handler

app = Flask(__name__)

@app.route('/jira', methods=['POST'])
def handle_jira():
    payload = request.get_json()
    response = create_jira_issue(payload)
    logger.info("Jira Issue Created: " + json.dumps(response))
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
