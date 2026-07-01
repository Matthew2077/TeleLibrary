"""
Bot Telegram CRUD di esempio.

Comandi disponibili:
    /start          - messaggio di benvenuto
    /help           - elenco comandi
    /add <testo>    - CREATE: aggiunge un nuovo elemento
    /list           - READ: mostra tutti i tuoi elementi
    /update <id> <nuovo testo> - UPDATE: modifica un elemento esistente
    /delete <id>    - DELETE: elimina un elemento

Avvio:
    1. Crea un bot con @BotFather su Telegram e copia il token.
    2. Esporta la variabile d'ambiente:  export BOT_TOKEN="il_tuo_token"
    3. Esegui:  python bot.py
"""

import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from database import init_db, SessionLocal
from models import Item

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ---------- CREATE ----------
async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "Uso: /add <testo>\nEsempio: /add Comprare il latte"
        )
        return

    title = " ".join(context.args)
    user_id = update.effective_user.id

    with SessionLocal() as session:
        item = Item(user_id=user_id, title=title)
        session.add(item)
        session.commit()
        session.refresh(item)
        await update.message.reply_text(f"✅ Aggiunto elemento #{item.id}: {item.title}")


# ---------- READ ----------
async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    with SessionLocal() as session:
        items = (
            session.query(Item)
            .filter(Item.user_id == user_id)
            .order_by(Item.id)
            .all()
        )

    if not items:
        await update.message.reply_text("Non hai ancora nessun elemento. Usa /add per crearne uno.")
        return

    lines = [f"#{item.id} — {item.title}" for item in items]
    await update.message.reply_text("📋 I tuoi elementi:\n" + "\n".join(lines))


# ---------- UPDATE ----------
async def update_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /update <id> <nuovo testo>\nEsempio: /update 3 Comprare il pane"
        )
        return

    raw_id, *rest = context.args
    new_title = " ".join(rest)
    user_id = update.effective_user.id

    if not raw_id.isdigit():
        await update.message.reply_text("L'id deve essere un numero. Esempio: /update 3 Nuovo testo")
        return

    item_id = int(raw_id)

    with SessionLocal() as session:
        item = (
            session.query(Item)
            .filter(Item.id == item_id, Item.user_id == user_id)
            .first()
        )
        if item is None:
            await update.message.reply_text(f"Nessun elemento trovato con id #{item_id}.")
            return

        item.title = new_title
        session.commit()
        await update.message.reply_text(f"✏️ Elemento #{item_id} aggiornato: {new_title}")


# ---------- DELETE ----------
async def delete_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Uso: /delete <id>\nEsempio: /delete 3")
        return

    item_id = int(context.args[0])
    user_id = update.effective_user.id

    with SessionLocal() as session:
        item = (
            session.query(Item)
            .filter(Item.id == item_id, Item.user_id == user_id)
            .first()
        )
        if item is None:
            await update.message.reply_text(f"Nessun elemento trovato con id #{item_id}.")
            return

        session.delete(item)
        session.commit()
        await update.message.reply_text(f"🗑️ Elemento #{item_id} eliminato.")


# ---------- COMANDI INFO ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Ciao! Sono un bot CRUD di esempio 🤖\n\n"
        "Posso aiutarti a gestire una semplice lista di elementi.\n"
        "Scrivi /help per vedere tutti i comandi disponibili."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Comandi disponibili:\n\n"
        "/add <testo> — crea un nuovo elemento\n"
        "/list — mostra i tuoi elementi\n"
        "/update <id> <testo> — modifica un elemento\n"
        "/delete <id> — elimina un elemento\n"
        "/help — mostra questo messaggio"
    )


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "Variabile d'ambiente BOT_TOKEN non impostata. "
            "Esegui: export BOT_TOKEN='il_tuo_token_da_BotFather'"
        )

    # Rimuove eventuali spazi, newline o caratteri di controllo (es. codici ANSI
    # incollati per errore) che possono finire nella variabile d'ambiente
    # quando il token viene copiato da terminali o editor con syntax highlighting.
    token = token.strip()
    cleaned = "".join(ch for ch in token if ch.isprintable())
    if cleaned != token:
        logger.warning(
            "BOT_TOKEN conteneva caratteri non stampabili che sono stati rimossi. "
            "Controlla come hai copiato/impostato il token."
        )
        token = cleaned

    init_db()

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_item))
    app.add_handler(CommandHandler("list", list_items))
    app.add_handler(CommandHandler("update", update_item))
    app.add_handler(CommandHandler("delete", delete_item))

    logger.info("Bot avviato. In ascolto di aggiornamenti...")
    app.run_polling()


if __name__ == "__main__":
    main()
