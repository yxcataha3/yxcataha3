import os
from loguru import logger
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from convert_tdata import convert_tdata

API_HASH = "7d376d6a24ab8bdcef00de57cf31778f"
API_ID = 2511669

sessions = []

for tdata in os.listdir("tdatas"):
    try:
        auth_key = convert_tdata(f"tdatas/{tdata}")[0]
    except Exception as err:
        logger.error(err)
    else:
        logger.success(f"{tdata} успешно конвертировано")

        sessions.append(StringSession(auth_key))

logger.info("Проверка аккаунтов")

for session in sessions[1:]:
    print(session)
    client = TelegramClient(
        session,
        api_hash=API_HASH,
        api_id=API_ID
    )

    try:
        client.connect()
        me = client.get_me()
    except Exception as err:
        logger.error(err)
    else:
        if me is None:
            logger.error("bad account")
            continue

        auth_key = client.session.save()
        with open(f"sessions/{auth_key[-10:]}.session", "w") as file:
            file.write(auth_key)

        logger.success(f"{me.first_name} — сохранён.")

