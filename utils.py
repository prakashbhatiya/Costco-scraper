""" This module for Utility """
import requests, os, json, logging

# Create and configure logger
logging.basicConfig(filename="logger.log", level = logging.ERROR,  format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()


# global variable
FOLDER_NAME = 'Data/'       # f'{os.getcwd()}/Data/followings/{USER_NAME}'
PATH = os.getcwd()
DEBUG = True


def debug(message: str="", type: str="Info", logger=None):
    """ function to add message to console

    Args:
        message (str, optional): message printed to be console.
        type (str, optional): type of longer
        logger (_type_, optional): logger to log in logfile
    """
    if DEBUG==True:
        print(f" {message}, {type} ")

    if logger:
       # Test messages
        logger.debug("Harmless debug Message")
        logger.info("Just an information")
        logger.warning("Its a Warning")
        logger.error("Did you try to divide by zero")
        logger.critical("Internet is down")

# >> function to process requests
def process_request( method: str, url: str, headers: str,  payload: dict ) -> dict:
        """This method for request

        Args:
            method (str): String
            url (str): String
            payload (str): String

        Returns:
            dict: return json data
        """
        try:
            response = requests.request(method, url, headers=headers , data=payload, timeout=20)
            return response
        except Exception as e:
            debug("Not getting response from request API", str(e))

# >> function to save response in json file
def save_response(text: dict, file: str, path) -> None:
    """ saving response to th json file for future investigation

    Args:
        text (str): text from the response
        file (str): name of the file to save
    """
    try:
        json_path = os.path.join( os.path.dirname(__file__), path)
        if not os.path.exists( json_path ):
            os.makedirs( json_path )

        with open(os.path.join( json_path, file), 'w', encoding='utf-8') as w:
            json.dump(text, w, indent=4)
    except Exception as e:
        debug("Exception::::", str(e), logger)