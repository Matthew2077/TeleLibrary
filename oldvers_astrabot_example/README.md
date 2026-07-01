# Telegram CRUD Bot (esempio)

Bot Telegram minimale che mostra le quattro operazioni CRUD (Create, Read,
Update, Delete) su una lista personale di elementi, salvata in SQLite tramite
SQLAlchemy 2.x (stesso stile che usi in LibraryTools: `Mapped` / `mapped_column`).

## Struttura

```
telegram_crud_bot/
├── bot.py          # logica del bot e handler dei comandi
├── database.py     # engine SQLAlchemy + sessionmaker
├── models.py       # modello Item (tabella items)
└── requirements.txt
```

## Setup

1. **Crea il bot su Telegram**
   - Apri Telegram, cerca `@BotFather`
   - Manda `/newbot`, segui le istruzioni
   - Copia il token che ti restituisce (es. `123456789:ABCdefGhIJKlmNoPQRstuVwxYZ`)

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Imposta il token come variabile d'ambiente**
   ```bash
   export BOT_TOKEN="il_tuo_token_qui"
   ```

4. **Avvia il bot**
   ```bash
   python bot.py
   ```

Il bot resta in polling: apri Telegram, cerca il tuo bot per username e
scrivigli `/start`.

## Comandi disponibili

| Comando | Operazione | Esempio |
|---|---|---|
| `/add <testo>` | **C**reate | `/add Comprare il latte` |
| `/list` | **R**ead | `/list` |
| `/update <id> <testo>` | **U**pdate | `/update 1 Comprare il pane` |
| `/delete <id>` | **D**elete | `/delete 1` |
| `/help` | — | mostra l'elenco comandi |

Ogni utente vede solo i propri elementi (filtrati per `user_id` Telegram),
quindi il bot funziona già correttamente anche con più persone che lo usano
insieme.

## Note / possibili estensioni

- Al momento usa il **polling** (`app.run_polling()`), perfetto per sviluppo
  locale. In produzione su un server si passa di solito ai **webhook**.
- Il database è un singolo file `bot.db` creato automaticamente al primo avvio.
- Spunti per estenderlo: paginazione su `/list`, conferma prima di `/delete`,
  bottoni inline (`InlineKeyboardMarkup`) invece di comandi testuali, o
  riportare la stessa logica in endpoint FastAPI riusando `models.py` /
  `database.py` così com'è.
