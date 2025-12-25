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

# Fungsi helper umum
import tkinter as tk


def center_window(window: tk.Tk | tk.Toplevel):
    """
    Center a Tkinter window on the screen.
    
    Args:
        window: Instance of Tk() or Toplevel()
    """
    window.update_idletasks()

    w = window.winfo_width()
    h = window.winfo_height()

    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()

    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)

    window.geometry(f"{w}x{h}+{x}+{y}")
    
def format_text(text: str) -> str:
    """Format text agar huruf pertama kapital"""
    return text.strip().capitalize()