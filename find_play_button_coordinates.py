import pyautogui
import time

print("Move your mouse over the Play Again button and wait...")
time.sleep(5)  # Gives you 5 seconds to move the mouse

x, y = pyautogui.position()
print(f"Mouse is at: {x}, {y}")
