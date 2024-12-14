import yaml
from typing import Any
from pydantic import BaseModel


class CfgButton(BaseModel):
    text: str
    url: str


class CfgGroup(BaseModel):
    # channel and group have the same config
    id: int
    url: str


class CfgBot(BaseModel):
    token: str
    username: str
    freechat_rate: int
    group: CfgGroup
    channel: CfgGroup


class Cfg(BaseModel):
    version: str
    buttons: list[CfgButton]
    images: list[str]
    greetings: list[str]
    bots: list[CfgBot]


def load(filename: str) -> Cfg:
    config = None
    with open(filename, 'rt') as fh:
        c = yaml.load(fh, yaml.SafeLoader)
        config = Cfg(**c)
    return config
