import modal
from modal import App, Image

t1 = modal.App("charre-1")

app = modal.App(
  "flask-server",
  image=modal.Image.debian_slim().pip_install("flask", "torch"),
)

gpu = "T4"
slim_torch = modal.Image.debian_slim(python_version="3.10").pip_install("torch", "torchvision", "Pillow").add_local_python_source("models")


@app.function(gpu=gpu, image=slim_torch, serialized=False, volumes={"/data": modal.Volume.from_name("test_data")})
def trigger_model():
  from models.test import run_model

  return run_model()


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

  @web_app.get("/model_endpoint")
  def model_endpoint():
    return trigger_model.remote()

  return web_app
