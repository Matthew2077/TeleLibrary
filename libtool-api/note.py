import requests
from exceptions import NotFoundError, AppError
import logging
logger = logging.getLogger(__name__)


def read_note(id: int):
    try:
        note_id = str(id)
        #print(type(id)) # debug

        # creating request:
        url = "http://127.0.0.1:8001/LibraryTools/v1/notes/"
        endpoint = url + note_id

        # Send request
        response = requests.get(endpoint)
        if response.status_code == 404:
            raise ValueError("qualcosa è andato storto")
        return response 
    
    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)
        raise Exception("errore generico")

def read_all_notes():
    try:
        # creating request
        url = "http://127.0.0.1:8001/LibraryTools/v1/notes/"

        # Send request
        response = requests.get(url)
        if response.status_code == 404:
            raise NotFoundError(f"Nothing found here")
        
        return response
        
    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)
        raise AppError("Internal server error")



leggi = read_note(3414)
# print(leggi)

leggi_tutto = read_all_notes()
# print(response.content)


def prova():
    try:
        print("A")
        raise ValueError("qualcosa è andato storto")
        print("B")
    except Exception as e:
        print("C:", e)
        raise Exception("errore generico")

