import os
from dotenv import dotenv_values 

def get_config(debug=False):
    try:
        return {
        **dotenv_values("default.env"),  # load shared development variables
        **dotenv_values("secrets.env"),  # load sensitive variables
        **os.environ  # override loaded values with environment variables
        }
    except:
        raise
