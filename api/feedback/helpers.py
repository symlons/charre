import json
from http import HTTPStatus

from flask import Response


def response_wrapper(
    code: HTTPStatus, body: dict | None = None, headers: dict | None = None
) -> Response:
    """
    Wraps the response in a clean and consistent way.

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
