from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from .utils import bytes_decode

try:
    from pydantic.v1 import BaseModel, Field
except ImportError:
    from pydantic import BaseModel, Field  # type: ignore[assignment]


class Config(BaseModel):
    bot_token: str = Field(alias="bottoken", min_length=1)
    response_delay: float = Field(alias="responsedelay", ge=0)
    response_chance: float = Field(alias="responsechance", gt=0, le=100)

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True


def from_ini(file_name: str) -> Config:
    content = bytes_decode(Path(file_name).read_bytes())
    config_parser = ConfigParser()
    config_parser.read_string(content)
    return Config.parse_obj(config_parser["DEFAULT"])
