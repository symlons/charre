import modal
from modal import App, Image
import subprocess
import os

t1 = modal.App("charre-1")


app = modal.App(
  "flask-server",
  image=modal.Image.debian_slim().pip_install("flask"),
)


@app.function(scaledown_window=3)
@modal.wsgi_app()
def flask_app():
  from flask import Flask, request

  web_app = Flask(__name__)

  @web_app.get("/")
  def home():
    return "Testing Flask server"

  @web_app.post("/test")
  def foo():
    return request.json

  return web_app
