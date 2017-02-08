# Stackcite API

A REST API web application for [stackcite.com](http://stackcite.com).

## Installation

Clone the latest Stackcite API and database repositories from GitHub:

```bash
localhost ~ $ git clone https://github.com/Kobnar/stackcite.api.git
localhost ~ $ git clone https://github.com/Kobnar/stackcite.data.git
```

Create and activate a new `virtualenv` directory:

```bash
localhost ~ $ virtualenv env --no-site-packages
localhost ~ $ source env/bin/activate
```

Run the included `setuptools` install scripts:

```bash
(env) localhost ~ $ cd stackcite.data && python setup.py develop
(env) localhost stackcite.data $ cd ../stackcite.api && python setup.py develop
```

Start the API using `pserve`:

```bash
(env) localhost stackcite.api $ pserve production.ini
```

The API will serve on `http://0.0.0.0:3030`.

## Running Tests

The Stackcite API repository is configured to use `nose2` with branch coverage
reports generated in `htmlcov`. To run these tests, execute the following
command:

```bash
(env) localhost stackcite.api $ nose2
```