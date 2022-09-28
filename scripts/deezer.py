import webbrowser

from queue import Queue
from sys import exit
from threading import Thread
from typing import Any, Optional

from fastapi import FastAPI
from httpx import get
from uvicorn import Config, Server
from typer import Option, Typer


DEEZER_CONNECT = "https://connect.deezer.com/oauth"
DEEZER_CONNECT_AUTH = f"{DEEZER_CONNECT}/auth.php"
DEEZER_CONNECT_TOKEN = f"{DEEZER_CONNECT}/access_token.php"

typer = Typer()


class DeezerAuthServer(Thread):
    """ A background server that generates Deezer access token. """

    def __init__(
        self,
        application_id: str,
        secret_id: str,
        queue: Queue,
    ) -> None:
        self._application_id = application_id
        self._secret_id = secret_id
        self._queue = queue

    def run(self, *args: Any, **kwargs: Any) -> None:
        api = FastAPI()

        @api.get("/")
        def _(code: Optional[str]) -> None:
            response = get(
                f"{DEEZER_CONNECT_TOKEN}"
                f"?app_id={self._application_id}"
                f"&secret={self._secret_id}"
                f"&code={code}"
                "&output=json"
            )
            result = response.json()
            token = result.get("access_token")
            self._queue.put(token)

        config = Config(api, port=8000)
        server = Server(config)
        server.run()


@typer.command("token")
def get_access_token(
    application_id: str = Option(...),
    secret_id: str = Option(...),
) -> None:
    queue = Queue()
    server = DeezerAuthServer(application_id, secret_id, queue)
    server.start()
    webbrowser.open(
        f"{DEEZER_CONNECT_AUTH}"
        f"?app_id={application_id}"
        f"&redirect_uri=localhost:8000"
        f"&perms=offline_access,email"
    )
    token = queue.get(block=True, timeout=None)
    print(token)
    exit()
