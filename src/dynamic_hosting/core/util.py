#!/usr/bin/env python3
import logging

from pathlib import Path
from logging import Logger


def rmdir(
        directory: Path
) -> None:
    logger: Logger = logging.getLogger(__name__)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
            logger.info('Removed file: <{item}>'.format(item=item))
        else:
            item.unlink()
    directory.rmdir()
    logger.info('Removed directory: <{directory}>'.format(directory=directory))
