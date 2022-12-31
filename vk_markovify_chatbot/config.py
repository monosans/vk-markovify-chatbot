from __future__ import annotations

from configparser import ConfigParser
from typing import AnyStr

from pydantic import BaseModel, Field


class Config(BaseModel):
    bot_token: str = Field(..., min_length=1)
    response_delay: float = Field(..., ge=0)
    response_chance: float = Field(..., gt=0, le=100)

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True


def from_ini(file_name: AnyStr) -> Config:
    config_parser = ConfigParser()
    config_parser.read(file_name, encoding="utf-8")
    cfg = config_parser["DEFAULT"]
    return Config(
        bot_token=cfg.get("BotToken"),
        response_delay=cfg.getfloat("ResponseDelay", 0),
        response_chance=cfg.getfloat("ResponseChance", 100),
    )
