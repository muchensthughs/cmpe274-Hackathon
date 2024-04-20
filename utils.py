import os, configparser

def load_credentials():
    ini_reader = configparser.ConfigParser()
    ini_reader.read("credential.ini")
    os.environ["OPENAI_API_KEY"] = ini_reader.get("general", "API_KEY")