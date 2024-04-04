import configparser

config = configparser.ConfigParser()
#config.read('Config/config.ini')
config.read('C:/Users/syeda/VA/venv/Scripts/Vision-The-Virtual-Assistant/Config/config.ini')
#This Method will load the key from config file
def getConfigKey(keyName):
    return config.get('api_keys', keyName)

api_key = getConfigKey("opanaiAPI")
print(api_key)
