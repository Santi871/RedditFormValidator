import configparser


def get_token(token_name, config_name='tokens.ini', section='tokens'):

    config = configparser.ConfigParser()
    config.read(config_name)
    token = config.get(section, token_name)
    return token
