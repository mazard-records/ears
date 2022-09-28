from os import environ

from httpx import Client
from pydantic import BaseModel


class LoginPayload(BaseModel):
    username: str
    password: str
    remember: bool = False

    @classmethod
    def from_environ(cls) -> "LoginPayload":
        return cls(
            username=environ.get("BEATPORT_USERNAME"),
            password=environ.get("BEATPORT_PASSWORD"),
        )


BASE_URL = "https://www.beatport.com"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"

def test_login() -> None:
    client = Client(base_url=BASE_URL)
    payload = LoginPayload.from_environ()
    # NOTE: force session to be filled with CSRF token.
    response = client.get("/api/my-beatport")
    response = client.get("/api/account")
    print("= Cookies")
    print(list(client.cookies.keys()))
    response = client.get(client.get("/api/csrfcheck")")
    response = client.post(
        "/api/account/login",
        json=payload.dict(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://www.beatport.com",
            "Referer": "https://www.beatport.com/",
            "User-Agent": USER_AGENT,
            "X-CSRFToken": client.cookies.get("_csrf_token"),
            "X-Requested-With": "XMLHttpRequest",
        }
    )
    print("= Login")
    print(response)
    response = client.get("/api/my-beatport")
    print("= My beatport")
    print(response.json())


if __name__ == "__main__":
    test_login()
