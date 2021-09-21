from secrets import client_secret, password
from basadobot import bot
from time import sleep
from prawcore.exceptions import RequestException, ServerError, ResponseException

if __name__ == '__main__':
    BasadoBot = bot(
        client_id = "1J2OALZQOi91tg",
        client_secret = client_secret,
        user_agent = "<BasadoBot:v2.0.1>",
        username = "BasadoBot",
        password = password
    )

    while True:
        try:
            BasadoBot.run()

        except RequestException:
            print("RequestException")
            sleep(10)

        except ServerError:
            print("504 HTTP response")
            sleep(10)

        except ResponseException:
            print("500 HTTP response")
            sleep(10)