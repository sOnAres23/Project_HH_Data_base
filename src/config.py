from configparser import ConfigParser


def config(filename=r"D:\PyCharm\Projects\Project_HH_Data_base\data\database.ini", section="postgresql"):
    """Функция для получения словаря с данными для подключения к БД"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db