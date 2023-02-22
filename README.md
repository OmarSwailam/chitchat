# Chit Chat Web APP
Django Web application for group chatting using websockets via Channels library for real time communication, where users can create or join chat rooms.

## How Chit Chat works ?
- Registration can be done using Name, Email and Password and optionally an image, then the user can login using that information.

- The user will be taken to the home page "index page", where he/she will be able to view all room, joined rooms or rooms created by him/her.

- Also, he/she will be able to create new rooms providing "room name" and optionally an image and a password.

- Accessing a room will view the chat messages, and the user will also be able to send messages.

### Tech used:
Python - Django - Channels library and web sockets for asynchronous communication - JavaScript - Bootstrap - HTML - CSS


## Running app

```

# Clone repository

# Create a virtualenv(optional)
  python3 -m venv env


# Install all dependencies
   pip install -r requirements.txt


# Activate the virtualenv
  source venv/bin/activate or .venv/bin/activate

# Run application
 ./manage.py runserver or python manage.py runserver

```

Author: Omar Swailam