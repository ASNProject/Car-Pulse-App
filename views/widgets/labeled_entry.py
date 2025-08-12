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

class LabeledEntry(tk.Frame):
    def __init__(self, parent, label_text, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.label = ttk.Label(self, text=label_text)
        self.label.pack(side="left", padx=5)
        
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.entry_var)
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
    
    def get_value(self):
        return self.entry_var.get()
    
    def set_value(self, value):
        self.entry_var.set(value)
