from configparser import ConfigParser
#from lib.log import logger

config_file = './config.ini'
#share_config_file = './share/config.ini'

config = ConfigParser()
config.read(config_file)

#share_config = init_share_config()

version = ''

path_sql = ""
param_sheet_name = ""

def get_version():
    return version

def check_config_section():
    if not config.has_section('common'):
        config.add_section('common')

    if not config.has_section('path'):
        config.add_section('path')

    if not config.has_section('param'):
        config.add_section('param')
            

    config.write(open(config_file, 'w'))

def get_config():
    global version, path_sql, param_sheet_name

    try:
        version = config.get('common', 'version')
    except Exception as e:
        #logger.warning(e)
        version = ''
        
    try:
        path_sql = config.get("path", "sql")
    except Exception as e:
        #logger.warning(e)
        path_sql = ""
        
    try:
        param_sheet_name = config.get("param", "sheet_name")
    except Exception as e:
        #logger.warning(e)
        param_sheet_name = ""
        
def reload_config():
    check_config_section()
    get_config()
    #check_config_valid()

if __name__ == '__main__':
    reload_config()
