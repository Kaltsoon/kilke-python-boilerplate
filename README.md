# Python boilerplate for Kilke

This repository contains boilerplate code, which can be used to establish basic communication with the `system-io` server.

## Installation

1. Install `pip` and [`virtualenv`](https://virtualenv.pypa.io/en/latest/installation/).

2. Create virtualenv by running `python3 -m viertualenv venv`.

3. Activate virtualenv by running `. venv/bin/activate`.

4. Install dependencies by running `pip install -r requirements.txt`

## Usage

First make sure that you have activated virtualenv by running `. venv/bin/activate`.

Boilerplate relies on `SYSTEM_ID` (id of the system you want to communicate with), `SYSTEM_IO_HOST` (`system-io` server host) and `SYSTEM_IO_PORT` (`system-io` server port) environment variables. You can start the program by running `SYSTEM_ID=<YOUR_SYSTEM_ID> SYSTEM_IO_HOST=<YOUR_SYSTEM_IO_HOST> SYSTEM_IO_PORT=<YOUR_SYSTEM_IO_PORT> python3 ./src/index.py`.
