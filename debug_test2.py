#!/usr/bin/env python3

import sys
import tempfile
import os
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
print(f"File exists check: {os.path.isfile(temp_path)}")

# Test the set_file_path method with debugging
print(f"Before set_file_path:")
print(f"  - Close button visible: {drop_box.close_button.isVisible()}")
print(f"  - Close button exists: {drop_box.close_button is not None}")
print(f"  - Drop box file_path: {drop_box.file_path}")

# Add debugging to the set_file_path method
if os.path.isfile(temp_path):
    print("File check passed")
    drop_box.file_path = temp_path
    drop_box.original_extension = os.path.splitext(temp_path)[1]
    filename = os.path.basename(temp_path)
    drop_box.label.setText(filename)
    print(f"Label updated to: {drop_box.label.text()}")
    
    # Show close button when file is set
    if drop_box.close_button:
        print("Close button exists, calling show()")
        drop_box.close_button.show()
        print(f"Close button visible after show(): {drop_box.close_button.isVisible()}")
    else:
        print("Close button is None!")
else:
    print("File check failed")

print(f"After set_file_path:")
print(f"  - Close button visible: {drop_box.close_button.isVisible()}")
print(f"  - Drop box file_path: {drop_box.file_path}")

os.unlink(temp_path)
