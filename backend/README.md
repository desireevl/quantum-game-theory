# Quantum Game Theory

### Running with Gunicorn (background workers)
```
pip install gunicorn

gunicorn "app:app" --workers=4 --bind=127.0.0.1:5000
```