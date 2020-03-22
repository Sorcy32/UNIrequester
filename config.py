"""
Использование: сonfig.get_setting('секция','данные')
"""
import configparser
import os

path = "data\settings.ini"


def createConfig(path):
    """ Создать конфиг файл """
    config = configparser.ConfigParser()
    config.add_section("Account")
    config.set("Account", "Login", "Login")
    config.set("Account", "Password", "Password")
    config.add_section('Network')
    config.set("Network", "AccessKey",
               "?accessKey=access_key")
    config.set("Network", "link",
               "https://support.russianpost.ru/sd/services/rest/get/")
    config.set("Network", "Certificate_name", 'data/cert.pfx')
    config.set("Network", "Certificate_pass", 'xxxxxxx')
    config.add_section("Paths")
    config.set("Paths", "InputFile", "links.txt")
    config.set("Paths", "PEM_certificate", "data/tmp_cert.pem")
    with open(path, "w") as config_file:
        config.write(config_file)


# Загрузить конфиг
def get_config(path):
    if not os.path.exists(path):
        createConfig(path)
        # Вернет объект конфига
    config = configparser.ConfigParser()
    config.read(path)
    return config


# Запрашиваем что-то из конфига
def get_setting(section, data):
    config = get_config(path)
    val = config.get(section, data)
    return val


if __name__ == "__main__":
    createConfig(path)
