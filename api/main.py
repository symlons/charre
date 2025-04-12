from http import HTTPStatus

from flask import Flask, request
from flask_cors import CORS

from helpers import response_wrapper
from models import Feedback

app = Flask(__name__)

# Allow cors origin source: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app, supports_credentials=True)


@app.route('/api/v1/labels', methods=['GET'])
def list_labels():

    # TODO: replace with mongodb query to fetch unique labels of training set
    labels = [
        "label1",
        "label2",
        "label3",
        "label4",
        "label5",
    ]

    return response_wrapper(
        code=HTTPStatus.OK,
        body={
            "labels": labels,
            "count": len(labels),
        },
    )


@app.route('/api/v1/feedback', methods=['POST'])
def post_feedback():
    data = request.get_json()

    try:
        feedback = Feedback(**data)
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={
                "error": str(e),
            },
        )

    # TODO: insert feedback into mongodb
    
    return response_wrapper(
        code=HTTPStatus.CREATED,
        body={
            "message": "Feedback received",
        },
    )
