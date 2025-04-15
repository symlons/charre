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
docker build -t streamlit-app .
```

Run the container:

```bash
docker run -p 8501:8501 streamlit-app 
```