import pyautogui
import time
import cv2
import numpy as np
import os

# Set paths to the images
GAME_OVER_TEMPLATE = os.path.join(os.getcwd(), "game_over.png")
DOWNLOAD_BUTTON_TEMPLATE = os.path.join(os.getcwd(), "download_button.png")
CLICK_X = 756
CLICK_Y = 496

# Set max games limit
MAX_GAMES = 80  # Change this to how many games you want to play

# Initialize game counter
game_count = 0

def find_image_on_screen(template_path, confidence=0.8):
    """Find an image on the screen and return its location."""
    if not os.path.exists(template_path):
        print(f"Error: File {template_path} not found!")
        return None

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Error: Could not read {template_path}. Check the file format and path.")
        return None

    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= confidence:
        return max_loc  # Return position of the detected image
    return None

def click_until_disappears(image_path, click_x, click_y, max_attempts=10, delay=1.5):
    """
    Clicks on a given location until the specified image disappears.
    """
    attempts = 0
    while attempts < max_attempts:
        if find_image_on_screen(image_path):
            print(f"Clicking at ({click_x}, {click_y}) - Attempt {attempts + 1}")
            pyautogui.click(click_x, click_y)
            time.sleep(delay)
        else:
            print(f"{image_path} is no longer visible.")
            return True
        attempts += 1

    print(f"Failed to remove {image_path} after {max_attempts} attempts.")
    return False

while game_count < MAX_GAMES:
    print(f"Watching for 'game_over.png'... (Game {game_count + 1}/{MAX_GAMES})")

    # Step 1: Wait for 'game_over.png' to appear
    while not find_image_on_screen(GAME_OVER_TEMPLATE):
        time.sleep(1)

    print("Game Over detected! Clicking to dismiss...")

    # Step 2-3: Click on 'game_over.png' until it disappears
    game_over_location = find_image_on_screen(GAME_OVER_TEMPLATE)
    if game_over_location:
        game_over_x, game_over_y = game_over_location[0] + 10, game_over_location[1] + 10
        click_until_disappears(GAME_OVER_TEMPLATE, game_over_x, game_over_y)

    # Step 4: Wait for 'download_button.png' to appear
    print("Watching for 'download_button.png'...")
    while not find_image_on_screen(DOWNLOAD_BUTTON_TEMPLATE):
        time.sleep(1)

    print("Download button detected! Clicking Play button at ...")

    # Step 5: Click at (the play button) until 'download_button.png' disappears
    click_until_disappears(DOWNLOAD_BUTTON_TEMPLATE, CLICK_X, CLICK_Y)

    # Increment game counter
    game_count += 1
    print(f"Game restarted successfully! Total games played: {game_count}/{MAX_GAMES}")

    time.sleep(3)  # Short delay before next game

print(f"Reached {MAX_GAMES} games. Script stopping.")
