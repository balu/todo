# TODO

A simple app for self-hosted TODO/Appointment tracking.

# INSTALL

This is a Python3 Flask app.

Create a virtual environment:
```bash
python3 -m venv .venv
```

Activate it:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Initialize database:
```bash
python app.py
```

Run application:
```bash
flask run
```

# USAGE

The app maintains the todo list in a `todos.db` sqlite database.

The app does not support authentication. Run the server on your private
server (For example, your tailnet) and access it using a browser.
