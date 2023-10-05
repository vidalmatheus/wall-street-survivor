# Wall Street Survivor Data Connector Service![Python Version](https://img.shields.io/badge/Python-3.11.4-blue)

This project uses [Django Ninja](https://django-ninja.rest-framework.com/) as its core.


# Python Script Documentation: tasks.py

This script defines several tasks that can be executed using the `invoke` library. Each task corresponds to a specific action related to a Django project. The script utilizes the `functools.wraps` decorator and the `invoke.task` decorator for task definition.

## Table of Contents
1. [Introduction](#introduction)
2. [Function Definitions](#function-definitions)
   - [requirements](#requirements)
   - [lint](#lint)
   - [format](#format)

## Introduction
The tasks defined in this script serve to automate common actions within a Django project. They make use of the `invoke` library to execute shell commands. The script contains the following functions:

## Function Definitions

### `requirements`: A task function to generate the `requirements.txt` file.

### `lint`: A task function to perform linting checks using `isort` and `black`.

### `format`: A task function to format the code using `isort` and `black`.


<i>Obs.: All the previous commands can be executed by:</i>

```bash
inv <task_name>
```

## Running

### Local:

```bash
source path/to/your/executable/python3.11.4-virtualenv
pip install -r requirements.txt
python ./manage runserver
```

### Testing:

This backend uses [Pytest](https://docs.pytest.org/en/7.4.x/) as testing framework. The main reasons are simplicity and performance. I found this article [here](https://www.browserstack.com/guide/pytest-vs-unittest#:~:text=pytest%20is%20known%20for%20its,for%20test%20discovery%20and%20setup.) a good one for comparison with Unittest.

It also uses `coverage-run` with `pytest-cov` for coverage testing reasons. I suggest running the tests by:

```bash
pytest --cov
```


## Some thoughts

Hey, gus! How's it going? I'm gonna leave some thoughts here about tech decisions:

- I like Django Ninja REST framework because it's fast, production-ready, and has built-in integration with Pydantic.

- I've routed the main endpoint to the NinjaAPI docs UI, making it easier for you all to test the backend's endpoints. Check it out!

- I've built this service with some good integration practices in mind, like using a memcache service for logging into the Wall Street Survivor platform. I've also mapped their endpoints using the Request as Objects (Command Pattern) because it ensures that the endpoints stay independent and can be accessed from anywhere in this backend. And last but not least, I've designed it as if it's going to connect with other platforms in the future. To make that happen, I'd suggest the Orchestration Pattern, which adds an intermediary layer to decide which platform to connect to for each new feature this backend might have, even if it's dealing with a bunch of different platforms.

Hope you guys enjoy!
