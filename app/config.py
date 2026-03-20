import os


class Config:
    APP_NAME = os.getenv("APP_NAME", "my-devops-app")
    APP_ENV = os.getenv("APP_ENV", "dev")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    MESSAGE = os.getenv("MESSAGE", "Hello from Docker")