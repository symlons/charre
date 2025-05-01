# Streamlit App

Simple Streamlit app with following functionailites:

- Upload new image
- Retrieve classification of image and display it
- Provide feedback form (thumbs up/down, if image was incorrectly classified allow user to manualy set label)
- Send feedback to the feedback API
  

## Development

Startup compose stack



Install dependencies

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Containerization

Build the container:

```bash
docker build -t charre-app:latest .
podman build -t charre-app:latest .
```

Run the container:

```bash
docker run --name charre-app -p 8501:8501 charre-app:latest
podman run --name charre-app -p 8501:8501 charre-app:latest
```
