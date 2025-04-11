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
```

Start server:

```bash
flask --app main.py --debug run
```
