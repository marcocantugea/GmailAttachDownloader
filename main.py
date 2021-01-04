# Author: Marco Cantu Gea
# Main program runner
# Version 0.0.1
from Configurations.Loader import Loader as ConfigLoader
from Google.Client import ClientLoader
from Google.Mail import EmailReader

def main():
    pass
    # config = ConfigurationLoader()
    # configuratoins=config.getConfigurations()
    # print(config.getConfig("mailQuery"))
    #
    # print(ConfigurationLoader.get_config("mailQuery"))
    # print(ConfigLoader.get_config("mailQuery"))
    #client = ClientLoader().getClient()
    email_reader=EmailReader()
    email_reader.getMessages()


main()