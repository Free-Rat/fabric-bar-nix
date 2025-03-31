import psutil
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.circularprogressbar import CircularProgressBar


def read_file(path):
    try:
        with open(path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


class BatteryWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.progress_bar_0 = CircularProgressBar(
            name="battery-progress-bar",
            pie=False,
            size=24,
            value=1 / 100,
            max_value=100,
            min_value=1,
        )
        self.progress_bar_1 = CircularProgressBar(
            name="battery-progress-bar",
            pie=False,
            size=24,
            value=1 / 100,
            max_value=100,
            min_value=1,
        )
        self.bat1 = Label(
            label=f"0",
            style="margin: 0px 6px 0px 0px; font-size: 12px",
        )
        self.bat0 = Label(
            label=f"0",
            style="margin: 0px 6px 0px 0px; font-size: 12px",
        )
        self.box = Box(
            spacing=4,
            name="battery-widget",
            style_classes="panel-box",
            children=(
                Overlay(child=self.progress_bar_0, overlays=self.bat0, name="overlay"),
                Overlay(child=self.progress_bar_1, overlays=self.bat1, name="overlay"),
            ),
        )
        self.add(self.box)

    def get_battery_info(self, battery):
        capacity = read_file(f"/sys/class/power_supply/{battery}/capacity")
        status = read_file(f"/sys/class/power_supply/{battery}/status")
        max_capacity = read_file(f"/sys/class/power_supply/{battery}/energy_full")
        current_capacity = read_file(f"/sys/class/power_supply/{battery}/energy_now")

        return capacity, status, max_capacity, current_capacity

    def on_update(self, *_):
        b1 = self.get_battery_info(battery="BAT1")
        b0 = self.get_battery_info(battery="BAT0")
        self.progress_bar_0.value = int(b0[0])
        # print("pb", self.progress_bar_0.value)
        self.progress_bar_1.value = int(b1[0])
        # print("pb", self.progress_bar_1.value)
        self.bat0.set_label(b0[0])
        self.bat1.set_label(b1[0])
        # print("l", self.bat0.get_label())
        # print("l", self.bat1.get_label())
        return
