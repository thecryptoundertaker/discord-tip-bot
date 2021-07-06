import os
from dotenv import dotenv_values 

def get_config(debug=False):
    try:
        config_dict = {
        **dotenv_values("default.env"),  # load shared development variables
        **dotenv_values("secrets.env"),  # load sensitive variables
        **os.environ  # override loaded values with environment variables
        }

        assert(config_dict['DISCORD_TOKEN'])
        assert(config_dict['SECRET_KEY'])

        return config_dict
    except:
        raise

config = get_config()
