#! /bin/sh

exec watchmedo auto-restart -R -p '*.py' -- python -m telegram_bot
