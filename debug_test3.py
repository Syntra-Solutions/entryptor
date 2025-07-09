#!/usr/bin/env python3

import sys
import tempfile
import os
from PyQt6.QtWidgets import QApplication
from src.gui.components.drop_box import DropBox

app = QApplication(sys.argv)

# Create drop box
drop_box = DropBox("Test")

# Check close button properties
cb = drop_box.close_button
print(f"Close button properties:")
print(f"  - isVisible(): {cb.isVisible()}")
print(f"  - isHidden(): {cb.isHidden()}")
print(f"  - isEnabled(): {cb.isEnabled()}")
print(f"  - size(): {cb.size()}")
print(f"  - pos(): {cb.pos()}")
print(f"  - parent(): {cb.parent()}")
print(f"  - text(): '{cb.text()}'")

# Try to show it
print("\nCalling show()...")
cb.show()

print(f"After show():")
print(f"  - isVisible(): {cb.isVisible()}")
print(f"  - isHidden(): {cb.isHidden()}")

# Let's also force a repaint
print("\nCalling repaint()...")
cb.repaint()
drop_box.repaint()

print(f"After repaint():")
print(f"  - isVisible(): {cb.isVisible()}")

# Check the parent widget
print(f"\nParent widget properties:")
print(f"  - isVisible(): {drop_box.isVisible()}")
print(f"  - size(): {drop_box.size()}")
