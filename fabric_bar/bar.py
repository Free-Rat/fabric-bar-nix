# fabric bar.py example
# https://github.com/Fabric-Development/fabric/blob/rewrite/examples/bar/bar.py
from cProfile import label
import psutil
from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.eventbox import EventBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.centerbox import CenterBox
from fabric.system_tray.widgets import SystemTray
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.hyprland.widgets import Language, ActiveWindow, Workspaces, WorkspaceButton

from widgets.volume import VolumeWidget

from widgets.battery import BatteryWidget

from fabric.utils import (
    FormattedString,
    bulk_replace,
    invoke_repeater,
    get_relative_path,
)


class StatusBar(Window):
    def __init__(
        self,
    ):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left top right",
            margin="10px 10px 0px 10px",  # up right down left
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )
        self.workspaces = Workspaces(
            name="workspaces",
            spacing=4,
            # buttons=None,
            buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=str(ws_id)),
        )
        self.active_window = ActiveWindow(name="hyprland-window")
        self.language = Language(
            formatter=FormattedString(
                "{replace_lang(language)}",
                replace_lang=lambda lang: bulk_replace(
                    lang,
                    (r".*Eng.*", r".*Ar.*"),
                    ("ENG", "ARA"),
                    regex=True,
                ),
            ),
            name="hyprland-window",
        )
        self.date_time = DateTime(
            name="date-time",
            formatters=("%I:%M %A %d-%m-%Y", "%I:%M", "%A", "%m-%d-%Y"),
        )
        self.system_tray = SystemTray(name="system-tray", spacing=4)

        self.ram_progress_bar = CircularProgressBar(
            name="ram-progress-bar", pie=False, size=24
        )
        self.cpu_progress_bar = CircularProgressBar(
            name="cpu-progress-bar", pie=False, size=24
        )
        self.progress_bars_overlay = Overlay(
            child=self.ram_progress_bar,
            overlays=[
                self.cpu_progress_bar,
                Label(" ", style="margin: 0px 6px 0px 0px; font-size: 12px"),
            ],
        )
        self.status_container = Box(
            name="widgets-container",
            spacing=4,
            orientation="h",
            children=self.progress_bars_overlay,
        )
        self.battery = BatteryWidget()
        self.status_container.add(VolumeWidget())  # if AUDIO_WIDGET is True else None
        self.status_container.add(self.battery)

        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=self.workspaces,
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=[
                    self.date_time,
                ],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[
                    self.active_window,
                    self.status_container,
                    # self.battery,
                    self.system_tray,
                    self.language,
                ],
            ),
        )

        invoke_repeater(1000, self.update_progress_bars)

        self.show_all()

    def update_progress_bars(self):
        self.ram_progress_bar.value = psutil.virtual_memory().percent / 100
        self.cpu_progress_bar.value = psutil.cpu_percent() / 100
        self.battery.on_update()
        return True


def main():
    bar = StatusBar()
    app = Application("bar", bar)
    app.set_stylesheet_from_file(get_relative_path("bar.css"))

    app.run()


if __name__ == "__main__":
    main()
