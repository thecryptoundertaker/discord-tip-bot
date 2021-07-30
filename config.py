from loguru import logger
import os
from dotenv import dotenv_values 

@logger.catch(reraise=True)
def get_config(debug=False):
    logger.debug("Getting config.")
    config_dict = {
    **dotenv_values("local/default.env"),  # load shared development variables
    **dotenv_values("local/secrets.env"),  # load sensitive variables
    **os.environ  # override loaded values with environment variables
    }

    assert(config_dict['DISCORD_TOKEN'])
    assert(config_dict['SECRET_KEY'])

    return config_dict

config = get_config()
