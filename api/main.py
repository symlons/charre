from http import HTTPStatus

from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from feedback.helpers import response_wrapper
from feedback.mock import mock_data
from feedback.models import Feedback
from feedback.mongo import MongoCollections, get_client
from base64 import b64decode

app = Flask(__name__)

# Allow cors origin source: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app, supports_credentials=True)

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "GET request successful"}), 200

@app.route("/labels", methods=["GET"])
def list_labels() -> Response:
    label_client = get_client(MongoCollections.LABELS)

    labels = label_client.distinct("label")
    labels = [label.lower() for label in labels]
    labels.sort()

    return response_wrapper(
        code=HTTPStatus.OK,
        body={
            "labels": labels,
            "count": len(labels),
        },
    )


@app.route("/feedback", methods=["POST"])
def post_feedback() -> Response:
    feedback_client = get_client(MongoCollections.FEEDBACK)
    data = request.get_json()

    try:
        data["image"] = b64decode(data["image"])
        feedback = Feedback(**data)
        result = feedback_client.insert_one(feedback.model_dump())
    except ValueError as e:
        print(e)
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={
                "error": str(e),
            },
        )

    return response_wrapper(
        code=HTTPStatus.CREATED,
        body={
            "message": "Feedback received",
            "id": str(result.inserted_id),
        },
    )


if __name__ == "__main__":
    mock_data()
    app.run(host="localhost", port=5001, debug=True)
