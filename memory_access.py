import pymem

def read_memory_bytes(_address: int, _len: int, _asInt: bool = True, _signed: bool = False) -> int:
    """
    Reads the bytes in "Super Mario World (USA) - Snes9x 1.62.3" at _address.
    For this specific emulator, the base pointer of the address has to be used
    To offset the actual address of the value.

    Args:
        _address: the address in memory
        _len: the number of bytes to read
        _asInt: If the value is returned as an integer or raw bytes
        _signed: If the value is interpreted as a signed integer

    Returns:
        bytes: the bytes at that location
    """
    pm = pymem.Pymem("snes9x-x64.exe")
    memory_value = pm.read_bytes(pm.base_address + _address, _len)
    if _asInt:
        memory_value = int.from_bytes(memory_value, signed=_signed)
    return memory_value

def write_byte(_address: int, _byte: bytes) -> None:
    """
    Writes the byte _value at _address in _process

    Args:
        _process: the process name
        _address: the address in memory
        _value: the value to write

    Returns:
        None
    """
    pm = pymem.Pymem("snes9x-x64.exe")
    pm.write_bytes(pm.base_address + _address, bytes(_byte), len(bytes(_byte)))

if __name__ == "__main__":
    ...
