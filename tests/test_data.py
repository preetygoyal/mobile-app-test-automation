"""Real credentials baked into the demo app itself (saucelabs/my-demo-app-rn),
taken from the app's own test constants -- not invented for this project."""

STANDARD_USER = {"username": "bob@example.com", "password": "10203040"}
LOCKED_OUT_USER = {"username": "alice@example.com", "password": "10203040"}
NO_MATCH_USER = {"username": "1@2.com", "password": "f-o-o"}

ERROR_USERNAME_REQUIRED = "Username is required"
ERROR_PASSWORD_REQUIRED = "Password is required"
ERROR_NO_MATCH = "Provided credentials do not match any user in this service."
ERROR_LOCKED_OUT = "Sorry, this user has been locked out."
