from flask import current_app

def with_config(config_key: str):
    """Annotation that takes in a config key as a string and tries to grab it from the current app. 
    Passes it as the last argument to the child function."""
    pass