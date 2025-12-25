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
from tkinter import ttk
from core import config, utils
from views.widgets.truck_canvas import TruckCanvas
from views.maps_view import MapsView
from core.serial_reader import SerialReader


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.configure(bg=config.THEME_COLOR)

        utils.center_window(self)

        self.serial_reader = SerialReader(port="/dev/cu.usbserial-0001", baudrate=115200)

        self.truck_canvas = TruckCanvas(self, serial_reader=self.serial_reader)
        self.truck_canvas.pack(fill="both", expand=True)

        self.open_btn = tk.Button(
            self,
            text="Buka Maps",
            command=self.open_maps,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black",
            activebackground="#dddddd",
            padx=25,
            pady=10,
            relief="flat",
        )

        # Posisi bawah tengah
        self.open_btn.place(
            relx=0.5,
            rely=0.93,
            anchor="center"
        )

        # Pastikan button selalu di atas Canvas
        self.open_btn.lift()

    def open_maps(self):
        MapsView(self, serial_reader=self.serial_reader)
