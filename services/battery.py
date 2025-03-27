from typing import Literal

from fabric import Service, Signal
from loguru import logger


class BatteryService(Service):
    """Service to interact with the PowerProfiles service."""

    @Signal
    def changed(self) -> None:
        """Signal emitted when battery changes."""

    instance = None

    @staticmethod
    def get_default():
        if BatteryService.instance is None:
            BatteryService.instance = BatteryService()

        return BatteryService.instance

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )


service = BatteryService()
