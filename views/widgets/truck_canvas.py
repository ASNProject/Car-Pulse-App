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

import requests
from PIL import Image, ImageTk
import os
from core import config


class TruckCanvas(tk.Canvas):
    def __init__(self, parent, serial_reader=None):
        super().__init__(
            parent,
            bg=config.THEME_COLOR,
            highlightthickness=0
        )

        self.truck_x = 0
        self.truck_y = 0
        self.tire_values = ["--"] * 4
        self.tire_status = ["N/A"] * 4
        self.lat = 0.0
        self.lon = 0.0

        self.load_assets()
        self.bind("<Configure>", self.on_resize)

        # IDs untuk update tanpa delete all
        self.truck_img_id = None
        self.tire_rects = [None] * 4
        self.tire_texts = [None] * 4
        self.gps_text_id = None
        self.road_rect_id = None
        self.road_center_dashes = []

        if serial_reader:
            serial_reader.register_callback(self.update_data)

    # Assets
    def load_assets(self):
        path = os.path.join("assets", "truck.png")
        self.truck_raw = Image.open(path)

    # Update data
    def update_data(self, data: dict):
        self.tire_values = [str(data.get(f"ban{i + 1}", "--")) for i in range(4)]
        self.tire_status = [data.get(f"status{i + 1}", "N/A") for i in range(4)]
        self.lat = data.get("lat", 0.0)
        self.lon = data.get("lon", 0.0)
        self.render()

        # Send to API
        # self.send_to_api()

    # Road
    def draw_road(self, w, h):
        road_width = int(w * 0.45)
        road_x1 = (w - road_width) // 2
        road_x2 = road_x1 + road_width

        if self.road_rect_id is None:
            self.road_rect_id = self.create_rectangle(
                road_x1, 0, road_x2, h,
                fill=config.ROAD_COLOR, outline=""
            )
        else:
            self.coords(self.road_rect_id, road_x1, 0, road_x2, h)

        # center dashed line
        center_x = w // 2
        dash_height = 40
        gap = 35
        y = 0

        # Jika belum ada dash, buat list
        if not self.road_center_dashes:
            while y < h:
                dash_id = self.create_rectangle(
                    center_x - 4, y, center_x + 4, y + dash_height,
                    fill="white", outline=""
                )
                self.road_center_dashes.append(dash_id)
                y += dash_height + gap
        else:
            for dash_id in self.road_center_dashes:
                self.coords(dash_id, center_x - 4, y, center_x + 4, y + dash_height)
                y += dash_height + gap

    # Truck
    def draw_truck(self, w, h):
        truck_width = int(w * 0.32)
        ratio = truck_width / self.truck_raw.width
        truck_height = int(self.truck_raw.height * ratio)

        # hanya buat image baru jika ukuran berubah
        if not hasattr(self, 'truck_img') or self.truck_img.width() != truck_width:
            img = self.truck_raw.resize((truck_width, truck_height), Image.LANCZOS)
            self.truck_img = ImageTk.PhotoImage(img)

            if self.truck_img_id is None:
                self.truck_img_id = self.create_image(self.truck_x, self.truck_y, image=self.truck_img)
            else:
                self.itemconfig(self.truck_img_id, image=self.truck_img)

        self.truck_x = w // 2
        self.truck_y = h // 2
        if self.truck_img_id is not None:
            self.coords(self.truck_img_id, self.truck_x, self.truck_y)

    # Tire Box
    def draw_tire_boxes(self, w, h):
        box_w, box_h = 140, 55
        tires = [(-0.26, -0.18), (0.26, -0.18), (-0.26, 0.10), (0.26, 0.10)]

        for i, (dx, dy) in enumerate(tires):
            x = self.truck_x + int(w * dx)
            y = self.truck_y + int(h * dy)
            color = "green" if self.tire_status[i] == "OK" else "red"

            if self.tire_rects[i] is None:
                self.tire_rects[i] = self.create_rectangle(
                    x - box_w // 2, y - box_h // 2, x + box_w // 2, y + box_h // 2,
                    fill=config.BOX_BG, outline=color, width=2
                )
                self.tire_texts[i] = self.create_text(
                    x, y,
                    text=f"Ban {i + 1}\n{self.tire_values[i]} PSI\n{self.tire_status[i]}",
                    fill="white", font=("Arial", 10, "bold"), justify="center"
                )
            else:
                self.coords(self.tire_rects[i], x - box_w // 2, y - box_h // 2, x + box_w // 2, y + box_h // 2)
                self.itemconfig(self.tire_rects[i], outline=color)
                self.itemconfig(self.tire_texts[i],
                                text=f"Ban {i + 1}\n{self.tire_values[i]} PSI\n{self.tire_status[i]}")
                self.coords(self.tire_texts[i], x, y)

        # gps_text = f"Lat: {self.lat:.4f}\nLon: {self.lon:.4f}"
        # if self.gps_text_id is None:
        #     self.gps_text_id = self.create_text(
        #         self.truck_x, self.truck_y - 120, text=gps_text,
        #         fill="yellow", font=("Arial", 12, "bold"), justify="center"
        #     )
        # else:
        #     self.coords(self.gps_text_id, self.truck_x, self.truck_y - 120)
        #     self.itemconfig(self.gps_text_id, text=gps_text)

    # Render
    def render(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 300 or h < 300:
            return

        self.draw_road(w, h)
        self.draw_truck(w, h)
        self.draw_tire_boxes(w, h)

    def on_resize(self, event):
        self.render()

    def send_to_api(self):
        url = "http://127.0.0.1:8000/api/carpulses"  # Ganti dengan real URL API
        body = {
            "user_id": "123",
            "b_front_left": self.tire_values[0],
            "b_front_right": self.tire_values[1],
            "b_back_left": self.tire_values[2],
            "b_back_right": self.tire_values[3],
            "s_front_left": self.tire_status[0],
            "s_front_right": self.tire_status[1],
            "s_back_left": self.tire_status[2],
            "s_back_right": self.tire_status[3],
            "latitude": str(self.lat),
            "longitude": str(self.lon),
        }

        try:
            response = requests.post(url, json=body, timeout=5)
            print("API response:", response.status_code, response.text)
        except Exception as e:
            print("Error mengirim data ke API:", e)
