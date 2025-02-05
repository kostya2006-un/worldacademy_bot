from telegram_bot.api.server import Server
from telegram_bot.core.settings import Settings

server = Server(
    server_host=Settings().server_host
)
