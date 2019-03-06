import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_key(key):
    return config['CONSTANTS'][key]


def set_key(key, value):
    config.set("CONSTANTS", key, value)
    with open('config.ini', "w") as config_file:
        config.write(config_file)
