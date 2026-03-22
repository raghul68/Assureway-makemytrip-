import os
import time

def take_screenshot(driver, test_name):
    """
    Utility function to take screenshots on test failure.
    Saves the screenshot in the 'screenshots' directory.
    """
    # Create screenshots directory if it doesn't exist
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
        
    # Generate unique filename with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filepath = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    
    # Capture and save screenshot
    try:
        driver.save_screenshot(filepath)
        print(f"Screenshot saved successfully at: {filepath}")
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")
