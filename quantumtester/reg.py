from typing import Optional
from winreg import (
    CreateKey,
    HKEY_LOCAL_MACHINE,
    OpenKey,
    SetValueEx,
    CloseKey,
    QueryValueEx,
    REG_DWORD,
    KEY_WRITE,
    KEY_READ,
)

REG_PATH = r"SYSTEM\ControlSet001\Control\PriorityControl"
DWORD_NAME = "Win32PrioritySeparation"


def set_reg(value: int) -> bool:
    """
    Set a DWORD value in the Windows Registry.

    Args:
        value (int): The value to set.

    Returns:
        bool: True if successful, False if there was an error.
    """
    try:
        # Create or open
        CreateKey(HKEY_LOCAL_MACHINE, REG_PATH)
        registry_key = OpenKey(HKEY_LOCAL_MACHINE, REG_PATH, 0, KEY_WRITE)

        # Set the DWORD value
        SetValueEx(registry_key, DWORD_NAME, 0, REG_DWORD, value)

        CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def get_reg() -> Optional[int]:
    """
    Get a DWORD value from the Windows Registry.

    Returns:
        int: The registry value if found, None if there was an error.
    """
    try:
        registry_key = OpenKey(HKEY_LOCAL_MACHINE, REG_PATH, 0, KEY_READ)

        # Query the DWORD value
        value, regtype = QueryValueEx(registry_key, DWORD_NAME)

        CloseKey(registry_key)
        return value
    except WindowsError:
        return None
