# repo-report

## Getting Started

1. Setup:
    1. Create a virtual environment with venv: `python3 -m venv .venv`
    2. Activate the virtual environment: `source .venv/bin/activate`
    3. Install dependencies from requirements file: `pip install -r requirements.txt`
2. Configure:
    1. Set environment variables in the `template.env` file with proper values.
    2. Rename `template.env` to `.env`: `mv template.env .env`
3. Run tests to check that config values are set, compose a test email message, and test smtp settings:
    1. `make test`
4. Run the application:
    1. `make run`

## Containerization

1. `make docker.build`
2. `make docker.run`

## 🐍 Running in Python 🐍

`python3 main.py --help` for more info.

Easier:

`make all` will load your .env, format, lint, test, and run the application.

## Contributing

Format, lint, and test before commiting:
`make precommit`

