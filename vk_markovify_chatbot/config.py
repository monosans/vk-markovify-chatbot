from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import attrs

from .utils import bytes_decode

if TYPE_CHECKING:
    from typing import Mapping

    from typing_extensions import Any, Self

if sys.version_info >= (3, 11):
    try:
        import tomllib
    except ImportError:
        # Help users on older alphas
        if not TYPE_CHECKING:
            import tomli as tomllib
else:
    import tomli as tomllib


@attrs.define(
    repr=False,
    weakref_slot=False,
    kw_only=True,
    eq=False,
    getstate_setstate=False,
    match_args=False,
)
class Config:
    bot_token: str = attrs.field(
        validator=attrs.validators.and_(
            attrs.validators.instance_of(str), attrs.validators.min_len(1)
        )
    )
    response_delay: float = attrs.field(
        converter=float, validator=attrs.validators.ge(0)
    )
    response_chance: float = attrs.field(
        converter=float,
        validator=attrs.validators.and_(
            attrs.validators.gt(0), attrs.validators.le(100)
        ),
    )

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any], /) -> Self:
        return cls(
            bot_token=mapping["bot_token"],
            response_delay=mapping["response_delay"],
            response_chance=mapping["response_chance"],
        )


def from_toml(file_name: str, /) -> Config:
    content = Path(file_name).read_bytes()
    config = tomllib.loads(bytes_decode(content))
    return Config.from_mapping(config)
