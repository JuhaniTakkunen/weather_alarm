import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    # https://pypi.org/project/python-dotenv/
    env_path = Path(__file__).parent / '.env'
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)
except ImportError:
    logger.warning("Unable to load library python-dotenv. This is "
                   "OK, IF all environment variables are defined.")
except Exception:
    logger.error("Unable to parse .env file. An example .env file is "
                 "found, named as .env_example")
    raise
