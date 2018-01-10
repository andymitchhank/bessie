# Bessie - Base API Client

[![Build Status](https://travis-ci.org/andymitchhank/bessie.svg?branch=master)](https://travis-ci.org/andymitchhank/bessie)

**Table of Contents**

* [About](#about)
* [Building Clients](#building-clients)
* [Installation](#installation)
* [License](#license)

## About 

Bessie is a small base framework for building client APIs. 

## Building Clients

The `BaseClient` class is designed to be subclassed. Each method is also designed to be overriden to include custom logic for specific APIs (such as injecting an authorization header by overriding the `_prepare_request` method).

## Installation

Bessie is avaialbe on [PyPI](https://pypi.python.org/pypi/bessie/). 

## License

Bessie is distributed under the terms of the [MIT License](https://choosealicense.com/licenses/mit).

