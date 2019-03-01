# parrot
An intelligent conversation engineering tool

## Table of Contents

* [Quick Start](#quick-start)
* [Migration](#migration)

## Quick start

Quick start:

- Create virtual environment `virtualenv venv`.
- Load the venv `source venv`.
- Install python packages `pip install -r requirement`.
- Add environment variable
  ```
  export SECRET_KEY=<a long string>
  export FLASK_APP=app
  export FLASK_ENV=development
  ```
- Initialize sqlite database `flask init-db`
- Run `flask run`.

## Migration

- If the schemas of the data models have been changed, run `flask db migrate -m "short message to describe what has been changed"`
- Run `flask db upgrade` to apply the latest schemas to the database
- Run `flask db downgrade` to apply previous schemas to the database
