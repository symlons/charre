# charre

MLOPS Project:

- [Feedback API](./api/README.md)
- [Streamlit App](./app/README.md)
- [AI Service](./model/README.md)
- [Sandbox Scripts](./sandbox/README.md)

Each directory has its own `requirements.txt` file and is independent of the others. The documentation about the services is in the respective directories.

**Default local project setup**

```shell
cd <project_root>

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Project management with `uv`

uv manages python dependencies and virtual environments with pyproject.toml. When using uv no manual virtual environment setup is required.
uv will auto detect virtual environment and dependencies and install them if they are missing and will also lock all dependencies. For more
info [see uv docs](https://docs.astral.sh/uv/).

```shell
# install all deps
uv sync --all-groups
# install for specific app
uv sync --group <app_name>

# run stuff
uv run python <path/to/script.py>
uv run streamlit run <path/to/app.py>
```

## Authors

- Conti Laura
- Häusermann Patrick
- Kost Fabio
- Truninger John
