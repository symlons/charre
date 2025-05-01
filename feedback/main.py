from base64 import b64decode
from http import HTTPStatus

from bson import ObjectId
from flask import Flask, Response, request
from flask_cors import CORS

from feedback.helpers import response_wrapper
from feedback.models import Feedback, FeedbackList
from feedback.mongo import MongoCollections, get_client

app = Flask(__name__)

# Allow cors origin source: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app, supports_credentials=True)


@app.route("/feedback/health", methods=["GET"])
def get_health() -> Response:
    """
    Health check endpoint
    """
    return response_wrapper(code=HTTPStatus.OK, body={"message": "OK"})


@app.route("/feedback/labels", methods=["GET"])
def list_labels() -> Response:
    """
    List all unique available labels in the database
    """
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


@app.route("/feedback/feedback", methods=["POST"])
def post_feedback() -> Response:
    """
    Adds a new feedback to the database
    """
    feedback_client = get_client(MongoCollections.FEEDBACK)
    data = request.get_json()

    try:
        data["image"] = b64decode(data["image"])
        feedback = Feedback(**data)
        result = feedback_client.insert_one(feedback.model_dump())
    except ValueError as e:
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


@app.route("/feedback/feedback", methods=["GET"])
def get_feedback() -> Response:
    """
    Lists all feedbacks in the database
    """
    feedback_client = get_client(MongoCollections.FEEDBACK)

    feedbacks = []
    try:
        for feedback in feedback_client.find(
            {}, {"_id": 1, "label": 1, "correct": 1, "correct_label": 1}
        ):
            feedback_id = str(feedback.pop("_id"))
            feedbacks.append(FeedbackList(**feedback, id=feedback_id).model_dump())
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={
                "error": str(e),
            },
        )

    return response_wrapper(
        code=HTTPStatus.OK,
        body={
            "feedback": feedbacks,
            "count": len(feedbacks),
        },
    )


@app.route("/feedback/feedback/<feedback_id>", methods=["GET"])
def get_feedback_by_id(feedback_id: str) -> Response:
    """
    Gets a feedback by its ID

    :param feedback_id: The ID of the feedback to get
    """
    feedback_client = get_client(MongoCollections.FEEDBACK)

    if not (feedback := feedback_client.find_one({"_id": ObjectId(feedback_id)})):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={
                "error": "Feedback not found",
            },
        )

    try:
        feedback = Feedback.model_validate(feedback)
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={
                "error": str(e),
            },
        )

    return response_wrapper(
        code=HTTPStatus.OK,
        body=feedback.model_dump(),
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
