<img src="https://raw.githubusercontent.com/gamma-lab/parrot/master/app/static/assets/img/logo-ny.svg?sanitize=true" height="200">
Parrot is an intelligent conversation engineering tool.

## Quick Start

- Setup the virtual environment and install required packages (tested with Python 3.6):
  ```
  virtualenv -p python3.6 venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Initialize sqlite database `flask init-db`
- Run `flask run` and go to http://127.0.0.1:5000/ to use Parrot

## Update Database

- Run `flask db upgrade` if the new models have been added.
