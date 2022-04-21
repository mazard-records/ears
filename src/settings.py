from pydantic import BaseSettings


class DeezerSettings(BaseSettings):
    pass


class EarsSettings(BaseSettings):
    deezer: DeezerSettings
