# Copyright 2025 ariefsetyonugroho
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk
from core import config, utils
from tkintermapview import TkinterMapView


class MapsView(tk.Toplevel):
    def __init__(self, parent, serial_reader=None):
        super().__init__(parent)

        self.title("Maps")
        self.geometry(config.WINDOW_SIZE)
        self.configure(bg="#1e1e1e")
        self.serial_reader = serial_reader

        utils.center_window(self)

        # Center window
        if hasattr(config, "center_window"):
            config.center_window(self)

        # TkinterMapView
        self.map_widget = TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        # Default location
        self.default_lat, self.default_lon = -6.2, 106.8
        self.map_widget.set_position(self.default_lat, self.default_lon)
        self.map_widget.set_zoom(12)

        # Pin marker
        self.pin = self.map_widget.set_marker(self.default_lat, self.default_lon, text="Truck")

        # SerialReader callback
        if serial_reader:
            serial_reader.register_callback(self.update_location)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_location(self, data: dict):
        lat = data.get("lat", self.default_lat)
        lon = data.get("lon", self.default_lon)

        # Update pin position
        if self.pin:
            self.pin.set_position(lat, lon)
        else:
            self.pin = self.map_widget.set_marker(lat, lon, text="Truck")

        # Optional: Center map to truck
        self.map_widget.set_position(lat, lon)

    def on_close(self):
        if self.serial_reader:
            self.serial_reader.unregister_callback(self.update_location)
        self.destroy()
