import io
import json
from base64 import b64decode
from http import HTTPStatus

from PIL import Image as PILImage
from flask import Flask, Response, request
from flask_cors import CORS

from predict import predict


def response_wrapper(
    code: HTTPStatus, body: dict | None = None, headers: dict | None = None
) -> Response:
    """
    Wraps the response in a clean and consistent way

    :param code: HTTPStatus
    :param body: dict
    :param headers: dict
    """
    if body:
        response = Response(
            response=json.dumps(body, default=str),
            status=code,
            mimetype="application/json",
        )
    else:
        response = Response(
            response=None,
            status=code,
            mimetype="application/json",
        )

    if headers:
        for key, value in headers.items():
            response.headers[key] = value
    return response


app = Flask(__name__)

# Allow cors origin source: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app, supports_credentials=True)


@app.route("/predict", methods=["POST"])
def post_predict() -> Response:
    """
    Predicts car brand from image
    """
    
    data = request.get_json()

    try:
        image = b64decode(data["image"])
        #print(type(image))
        image = PILImage.open(io.BytesIO(image)).convert("RGB")
        result = predict(image)
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
            "label": result,
            "accuracy": 0.99
        },
    )

    
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
