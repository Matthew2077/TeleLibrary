from telegram import Update
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Stato della conversazione
WAITING_FOR_ID = 1 # stato dove il bot aspetta l'utente che scriva lid

async def view_note_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Perfavore inserisci l'ID della nota che desideri visualizzare:")
    return WAITING_FOR_ID

async def view_note_receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if not user_input.isdigit():
        await update.message.reply_text("⚠️ L'ID deve essere un numero. Riprova o usa /cancel.")
        return WAITING_FOR_ID  # rimane in attesa

    note_id = int(user_input)

    # qui richiami la tua funzione esistente che chiama LibraryTools API
    note_data = get_note_by_id(note_id)  # la tua funzione già esistente, ma parametrica

    if note_data is None:
        await update.message.reply_text(f"❌ Nessuna nota trovata con ID {note_id}.")
        return ConversationHandler.END

    testo = (
        f"📚 **Titolo**: {note_data['title']}\n"
        f"📅 **Data di creazione**: {note_data['creation_date']}\n"
        f"📝 **Contenuto**: {note_data['content']}\n"
        f"📝 **FULL**: {note_data}"
    )
    await update.message.reply_text(testo, parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operazione annullata.")
    return ConversationHandler.END

# Registrazione dell'handler
view_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("view", view_note_start)],
    states={
        WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, view_note_receive_id)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(view_conv_handler)