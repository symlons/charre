from base64 import b64decode
from http import HTTPStatus

from bson import ObjectId
from flask import Flask, Response, request
from flask_cors import CORS
from pymongo.errors import PyMongoError

from feedback.helpers import response_wrapper
from feedback.models import Feedback, FeedbackList, FeedbackPatch
from feedback.mongo import MongoCollections, get_client, get_collection

app = Flask(__name__)

# Allow cors origin source: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app, supports_credentials=True)


@app.route("/feedback/readiness", methods=["GET"])
def get_readiness() -> Response:
    """
    Readiness check endpoint
    """
    try:
        client = get_client(timeout=2000)
        client.admin.command("ping")
    except PyMongoError:
        return response_wrapper(
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={
                "error": "MongoDB connection error",
            },
        )
    return response_wrapper(code=HTTPStatus.OK, body={"message": "OK"})


@app.route("/feedback/liveness", methods=["GET"])
def get_liveness() -> Response:
    """
    Liveness check endpoint
    """
    return response_wrapper(code=HTTPStatus.OK, body={"message": "OK"})


@app.route("/feedback/labels", methods=["GET"])
def list_labels() -> Response:
    """
    List all unique available labels in the database
    """
    label_client = get_collection(MongoCollections.LABELS)

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


@app.route("/feedback/labels", methods=["POST"])
def post_labels() -> Response:
    """
    Adds a new label to the database
    """
    label_client = get_collection(MongoCollections.LABELS)
    data = request.get_json()

    try:
        label = data["label"].lower().strip()
        if label_client.find_one({"label": label}):
            return response_wrapper(
                code=HTTPStatus.BAD_REQUEST,
                body={
                    "error": "Label already exists",
                },
            )
        label_client.insert_one({"label": label})
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={
                "error": str(e),
            },
        )
    return response_wrapper(
        code=HTTPStatus.CREATED,
        body={
            "message": "Label created",
            "label": label,
        },
    )


@app.route("/feedback/feedback", methods=["POST"])
def post_feedback() -> Response:
    """
    Adds a new feedback to the database
    """
    feedback_client = get_collection(MongoCollections.FEEDBACK)
    data = request.get_json()

    try:
        data["image"] = b64decode(data["image"])
        feedback = Feedback(**data)
        feedback.label = feedback.label.lower().strip()
        feedback.trained = False
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
    feedback_client = get_collection(MongoCollections.FEEDBACK)

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
    feedback_client = get_collection(MongoCollections.FEEDBACK)

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


@app.route("/feedback/feedback/<feedback_id>", methods=["PATCH"])
def patch_feedback_by_id(feedback_id: str) -> Response:
    """
    Updates a feedback by its ID

    :param feedback_id: The ID of the feedback to update
    """
    feedback_client = get_collection(MongoCollections.FEEDBACK)
    data = request.get_json()

    try:
        feedback = FeedbackPatch(**data)
        feedback_client.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$set": feedback.model_dump()},
        )
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={
                "error": str(e),
            },
        )
    return response_wrapper(
        code=HTTPStatus.OK,
        body={
            "message": "Feedback updated",
            "id": feedback_id,
        },
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
