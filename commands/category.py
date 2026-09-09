



async def get_categories_list()


    note = read_note(note_id)
    # decodifica dati (sono bytes)
    note_data = json.loads(note.content.decode('utf-8'))

read_all_categories