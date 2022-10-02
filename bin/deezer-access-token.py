import argparse
import webbrowser

from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue
from threading import Thread
from typing import Any
from urllib.parse import urlparse


from httpx import get


DEEZER_CONNECT = "https://connect.deezer.com/oauth"
DEEZER_CONNECT_AUTH = f"{DEEZER_CONNECT}/auth.php"
DEEZER_CONNECT_TOKEN = f"{DEEZER_CONNECT}/access_token.php"


class DeezerAuthServer(Thread):
    """ A background server that generates Deezer access token. """

    def __init__(
        self,
        application_id: str,
        secret_id: str,
        queue: Queue,
    ) -> None:
        super().__init__()
        self._application_id = application_id
        self._secret_id = secret_id
        self._queue = queue
        self._server = None

    def shutdown(self) -> None:
        self._server.shutdown()

    def run(self, *args: Any, **kwargs: Any) -> None:
        this = self
        class DeezerRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                query = urlparse(self.path).query
                components = dict(component.split("=") for component in query.split("&"))
                code = components.get("code")
                response = get(
                    f"{DEEZER_CONNECT_TOKEN}"
                    f"?app_id={this._application_id}"
                    f"&secret={this._secret_id}"
                    f"&code={code}"
                    "&output=json"
                )
                result = response.json()
                token = result.get("access_token")
                this._queue.put(token)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

        self._server = HTTPServer(("localhost", 8080), DeezerRequestHandler)
        self._server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Server for generating Deezer API access token",
    )
    parser.add_argument('--application_id', help="Deezer application id")
    parser.add_argument('--secret_id', help="Deezer secret id")
    args = parser.parse_args()
    application_id = args.application_id
    secret_id = args.secret_id
    if application_id is None or secret_id is None:
        raise ValueError("Missing application and secret ids")
    queue = Queue()
    print(f":: start DeezerAuthServer in background")
    server = DeezerAuthServer(application_id, secret_id, queue)
    server.start()
    print(f":: open Deezer connect")
    webbrowser.open(
        f"{DEEZER_CONNECT_AUTH}"
        f"?app_id={application_id}"
        f"&redirect_uri=http://localhost:8080/redirect"
        f"&perms=offline_access,email"
    )
    token = queue.get(block=True, timeout=None)
    print(f":: terminate background server")
    server.shutdown()
    server.join()
    print(f":: Your Deezer API access token: {token}")
