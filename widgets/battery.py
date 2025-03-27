from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

# import services
#
# print(services.battery_service)
# from services import battery_service
from services.battery import service


class BatteryWidget(Box):
    """A widget to display the current battery status."""

    def __init__(
        self,
        bar,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="battery",
            **kwargs,
        )
