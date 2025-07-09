#!/usr/bin/env python3

import sys
import tempfile
from PyQt6.QtWidgets import QApplication
from src.gui.components.drop_box import DropBox

app = QApplication(sys.argv)

# Create drop box
drop_box = DropBox("Test")

# Create temp file  
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write('test content')
    temp_path = f.name

print(f"Temp file: {temp_path}")
print(f"File exists: {temp_path}")

# Test the set_file_path method
print(f"Before set_file_path - Close button visible: {drop_box.close_button.isVisible()}")
print(f"Drop box file_path: {drop_box.file_path}")

drop_box.set_file_path(temp_path)

print(f"After set_file_path - Close button visible: {drop_box.close_button.isVisible()}")
print(f"Drop box file_path: {drop_box.file_path}")
print(f"Drop box label text: {drop_box.label.text()}")

import os
os.unlink(temp_path)
