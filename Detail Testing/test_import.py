import sys
import os
# Add current directory to path
sys.path.append(os.getcwd())

try:
    from pages.base_page import BasePage
    from selenium.webdriver.common.by import By
    print("BasePage imported successfully")
    print(f"By: {By}")
    bp = BasePage(None)
    print("BasePage instance created")
except Exception as e:
    print(f"Import Error: {e}")
    import traceback
    traceback.print_exc()
