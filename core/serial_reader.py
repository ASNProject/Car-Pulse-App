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
import serial
import threading
import json

class SerialReader:
    def __init__(self, port="COM5", baudrate=115200, callbacks=None):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.ser.reset_input_buffer()
        self.callbacks = callbacks or []  # selalu list
        threading.Thread(target=self._read_loop, daemon=True).start()

    def register_callback(self, func):
        if func not in self.callbacks:
            self.callbacks.append(func)

    def unregister_callback(self, func):
        if func in self.callbacks:
            self.callbacks.remove(func)

    def _on_data_received(self, data):
        for cb in self.callbacks:
            cb(data)

    def _read_loop(self):
        while True:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    print("Raw line:", line)
                if line.startswith("{") and line.endswith("}"):
                    data = json.loads(line)
                    self._on_data_received(data)
            except Exception as e:
                print("Serial error:", e)
