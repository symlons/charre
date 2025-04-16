# Feedback API

A simple REST API which provides endpoints for feedback collection and label informations.

## Development

Startup compose stack

```bash
docker compose up -d
podman compose up -d
```

You can then connect with MongoDB Compass like the following:

```text
mongodb://mongo:mongo@localhost:27017/
```

Install dependencies

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# or with uv
uv sync --group api
```

Start server and add mocking data:

```bash
python main.py
python mock.py

# or with uv
uv run python main.py
uv run python mock.py
```

### Containerization

Build the container:

```bash
docker build -t feedback-api:latest .
podman build -t feedback-api:latest .
```

Run the container:

```bash
docker run --name feedback-api -p 5000:5000 feedback-api:latest
podman run --name feedback-api -p 5000:5000 feedback-api:latest
```
