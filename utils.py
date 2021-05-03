import dotenv
import re

REGEX = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


async def dotenv_adjustment(key, value):
    dotenv.set_key("config.env", str(key).upper(), value)


def check_int(m):
        try:
            int(m.content)
            return True
        except ValueError:
            return False


def check_ip(m):
        return re.search(REGEX, m.content)
