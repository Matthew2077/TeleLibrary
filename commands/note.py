from libtoolapi.note import read_note
import json
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler, #input e output user
    filters,
    MessageHandler, 
)


# COMANDO LEGGI NOTA
STATUS_VIEW_ID = 1 # stato dove il bot aspetta l'utente che scriva l'id

async def view_note_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Perfavore inserisci l'ID della nota che desideri visualizzare:")
    return STATUS_VIEW_ID

async def view_note_exec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if not user_input.isdigit(): # qui inserire una funzione adatta poi. 
        await update.message.reply_text("⚠️ L'ID deve essere un numero. Riprova o usa /cancel.")
        return STATUS_VIEW_ID  # rimane in attesa

    note_id = int(user_input)

    note = read_note(note_id)
    # decodifica dati (sono bytes)
    note_data = json.loads(note.content.decode('utf-8'))

    if note_data is None:
        await update.message.reply_text(f"❌ Nessuna nota trovata con ID {note_id}.")
        return ConversationHandler.END

    titolo = note_data.get("title")
    contenuto = note_data.get("content")
    data_creazione = note_data.get("creation_date")

    await update.message.reply_text(
         f"📚 **Titolo**: {titolo}\n"
         f"📅 **Data di creazione**: {data_creazione}\n"
         f"📝 **Contenuto**: {contenuto}\n"
         f"📝 **FULL**: {note_data}\n"
         )
    return ConversationHandler.END




# funzione usata da tutti qui, il cancel. 
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operazione annullata.")
    return ConversationHandler.END



# CONV HANDLER DI VIEW:
view_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("view", view_note_start)],
    states={
        STATUS_VIEW_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, view_note_exec)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)




# CREATE NOTE:

# curl -X 'POST' \   'http://127.0.0.1:8001/LibraryTools/v1/notes/' \   
# -H 'accept: application/json' \   
# -H 'Content-Type: application/json' \   
# -d '{   "title": "string",   "content": "string",  
#  "category_id": 0,   "author_id": 0,   "tag_ids": [     0   ] }'

# INDICA I PASSAGGI
STATUS_CREATE_TITLE = 1 # primo passaggio
STATUS_CREATE_CONTENT = 2 # secondo passaggio

async def cn_title(update: Update, context: ContextTypes.DEFAULT_TYP):
    await update.message.reply_text("Benvenuto nella procedura per creare una nuova nota pubblica. \nTi chiedero' una serie di parametri per creare la nota, perfavore rispondi ad ogni domanda. \n\nScrivi il titolo titolo della nuova nota:")
    return STATUS_CREATE_TITLE

async def cn_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text  # salva la risposta precedente
    await update.message.reply_text("Inserisci il contenuto testuale della nota (no immagini): ")
    return STATUS_CREATE_CONTENT

async def create_note_exec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["content"] = update.message.text # context si porta dietro anche title e content
    await update.message.reply_text(f"Titolo: {context.user_data['title']}\nContenuto: {context.user_data['content']}")
    return ConversationHandler.END


# CONV HANDLER DI CREATE:
create_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("create", cn_title)],
    states={
        STATUS_CREATE_TITLE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, cn_content)],
        STATUS_CREATE_CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_note_exec)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)