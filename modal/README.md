# AI Service

Simple AI service with [modal](https://modal.com/) with a REST API to classify images.

Outline:
The aim of this work is to deploy the classification model on serverless GPU functions by using Modal.
On Modal we will deploy the model and provide an endpoint that serves the model.
The benfit of using serverless functions is that expesnive GPU resources are only loaded as they are needed, this helps reduce costs significantly.


ScratchNotes:
WSGI vs ASGI vs fastapi_endpoint in modal?
HTMLResponse
define timeout
ephemeral disk
modal deploy vs modal run
modal shell
container_idle_timeout
how to limit scaling / autoscaling
what are default scaledown_window, min_containers, buffer_containers set to? scaledown_window default: 60s after that the container is no longer warm and new requests require a cold start
security?


OutOfSCope:
Streaming Endpoint


TODOS:
setup volume for model weights
add basic http endpoint
let http endpoint trigger gpu function with demo model
Define requirements.txt

To run:
modal serve basic.py
