import requests
from exceptions import NotFoundError, AppError
import logging

logger = logging.getLogger(__name__)


def read_note(note_id: int):
    try:
        id = str(note_id)
        #print(type(id)) # debug

        # creating the request:
        endpoint = "http://127.0.0.1:8001/LibraryTools/v1/notes/"
        url = endpoint + id

        # Send request
        response = requests.get(url)
        if response.status_code == 404:
            raise NotFoundError(f"Note {note_id} not found")
        
        return response

    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)
        raise AppError("Internal server error")
    



response = read_note(1)
print(response.content)

