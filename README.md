# Python boilerplate for [kilke](https://github.com/Kaltsoon/kilke)

This repository contains boilerplate code, which can be used to establish basic communication with the kilke's `system-io` server.

## Installation

1. Install `pip` and [`virtualenv`](https://virtualenv.pypa.io/en/latest/installation/).

2. Create virtualenv by running `python3 -m virtualenv venv`.

3. Activate virtualenv by running `. venv/bin/activate`.

4. Install dependencies by running `pip install -r requirements.txt`

5. Create a file named `.env` into the project's root folder, and define values for `SYSTEM_ID` (id of the system you want to communicate with), `SYSTEM_IO_HOST` (`system-io` server host) and `SYSTEM_IO_PORT` (`system-io` server port) environment variables in the following manner:

```
SYSTEM_ID=<YOUR_SYSTEM_ID>
SYSTEM_IO_HOST=<YOUR_SYSTEM_IO_HOST>
SYSTEM_IO_PORT=<YOUR_SYSTEM_IO_PORT>
```

## Usage

First make sure that you have activated virtualenv by running `. venv/bin/activate`. After virtualenv has been activated ou can start the program by running `python3 ./src/index.py`.
