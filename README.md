# Python boilerplate for [kilke](https://github.com/Kaltsoon/kilke)

This repository contains boilerplate code, which can be used to establish basic communication with the kilke's `system-io` server.

## Installation

1. Install `pipenv` by running `sudo apt install pipenv` or by following the [installation instructions](https://github.com/pypa/pipenv#installation).

2. Install dependencies by running `pipenv install`

3. Create a file named `.env` into the project's root folder, and define values for `SYSTEM_ID` (id of the system you want to communicate with), `SYSTEM_IO_HOST` (`system-io` server host) and `SYSTEM_IO_PORT` (`system-io` server port) environment variables in the following manner:

```
SYSTEM_ID=<YOUR_SYSTEM_ID>
SYSTEM_IO_HOST=<YOUR_SYSTEM_IO_HOST>
SYSTEM_IO_PORT=<YOUR_SYSTEM_IO_PORT>
API_URL=<API_URL>
```

## Usage

Run `pipenv run python3 ./src/index.py` to start the `index.py` script.
