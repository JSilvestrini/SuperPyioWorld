import pydirectinput
import time
import win32gui

def find_activate_window() -> None:
    """
    Function used to activate the emulator game window

    Args:
        None

    Returns:
        None
    """
    hwnd = win32gui.FindWindow(None, "Super Mario World (USA) - Snes9x 1.62.3")
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)
        press_keys(['['] * 12)
        time.sleep(.1)
    else:
        "Window Not Found"

def get_region() -> tuple:
    hwnd = win32gui.FindWindow(None, "Super Mario World (USA) - Snes9x 1.62.3")
    if hwnd:
        win32gui.MoveWindow(hwnd, 0, 0, 512, 512, True)
        region = win32gui.GetClientRect(hwnd)
        region = (512 - region[2], 512 - region[3], region[2], 512)
        return region

def press_keys(keys: list) -> None:
    """
    Function used to 'press' down multiple keys in succession

    Args:
        key: the list of keys to press

    Returns:
        None
    """
    for i in keys:
        pydirectinput.keyDown(i, _pause=False)
        time.sleep(0.08)
        pydirectinput.keyUp(i, _pause=False)

def hold_key(keys: list, t: float = 4.0) -> None:
    """
    Function used to 'press' down multiple keys in succession

    Args:
        key: the list of keys to press

    Returns:
        None
    """
    for i in keys:
        pydirectinput.keyDown(i, _pause=False)
        time.sleep(t)
        pydirectinput.keyUp(i, _pause=False)

def press_combos(keys: list) -> None:
    """
    Function used to 'press' down multiple keys at the same time

    Args:
        key: the list of keys to press

    Returns:
        None
    """
    for i in keys:
        pydirectinput.keyDown(i, _pause=False)
    time.sleep(0.08)
    for i in keys:
        pydirectinput.keyUp(i, _pause=False)

def enter_stage(left_right):
    if left_right:
        press_keys(['right'])
        time.sleep(1.2)
        press_keys(['left'])
        time.sleep(1.2)
        press_keys(['v'])
    else:
        press_keys(['left'])
        time.sleep(1.2)
        press_keys(['right'])
        time.sleep(1.2)
        press_keys(['v'])