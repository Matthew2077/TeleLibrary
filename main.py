from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
import logging
from commands.note import view_conv_handler, create_conv_handler
import os
from dotenv import load_dotenv




# LOGGING SET UP
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


logger = logging.getLogger(__name__)

# COMANDO START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Ciao! Sono un bot in fase di sviluppo 🤖\n\n"
        "La mia specialita' sono le note, potrai vedere, creare e condividere tutte le note che vuoi\n"
        "Developer: https://github.com/Matthew2077"
    )

    
load_dotenv() # carica le variabili

# BASIC MAIN
def main() -> None:
    
    token = os.getenv("BOT_TOKEN")
    print(token)

    if not token:
        raise RuntimeError(
            "Variabile d'ambiente BOT_TOKEN non impostata. "
            "Esegui: export BOT_TOKEN='il_tuo_token_da_BotFather'"
        )

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(view_conv_handler)
    app.add_handler(create_conv_handler)


    logger.info("Bot avviato. In ascolto di aggiornamenti...")
    app.run_polling()


if __name__ == "__main__":
    main()



