from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def add_permission(
    path: Path, permission: int, /, *, missing_ok: bool = False
) -> None:
    try:
        current_permissions = path.stat().st_mode
        new_permissions = current_permissions | permission
        if current_permissions != new_permissions:
            path.chmod(new_permissions)
            logger.info(
                "Changed permissions of %s from %o to %o",
                path,
                current_permissions,
                new_permissions,
            )
    except FileNotFoundError:
        if not missing_ok:
            raise


def create_or_fix_dir(path: Path, /, *, permission: int) -> None:
    try:
        path.mkdir(parents=True)
    except FileExistsError:
        if not path.is_dir():
            msg = f"{path} is not a directory"
            raise ValueError(msg) from None
        add_permission(path, permission)
