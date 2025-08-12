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
from core import config
from controllers.user_controller import UserController
from views.widgets.labeled_entry import LabeledEntry

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.configure(bg=config.THEME_COLOR)

        self.controller = UserController()

        # Username input
        self.username_input = LabeledEntry(self, "Username:")
        self.username_input.pack(fill="x", pady=5, padx=10)

        # Email input
        self.email_input = LabeledEntry(self, "Email:")
        self.email_input.pack(fill="x", pady=5, padx=10)

        # Save button
        save_btn = ttk.Button(self, text="Simpan Data", command=self.save_data)
        save_btn.pack(pady=10)

    def save_data(self):
        username = self.username_input.get_value()
        email = self.email_input.get_value()
        self.controller.save_user(username, email)
