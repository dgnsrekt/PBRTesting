Playing around with the idea of parameterized based regression tests.


REQUIRED Environmental Variables
---

```
PORT=5000
SAMPLES=100
```

RUN IT
```
poetry install
poetry shell
python3 main.py # Runs a simple Rest API built with FASTAPI.
pytest # Runs tests on endpoints and methods.
```
