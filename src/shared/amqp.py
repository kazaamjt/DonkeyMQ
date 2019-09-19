"""
A collection fo usefull functions that help with AMQP communication.
"""

def str_to_bytes(string: str) -> bytes:
    return string.encode("utf-8")

def int_to_bytes(integer: int) -> bytes:
    return integer.to_bytes(1, byteorder="big", signed=False)

def bytes_to_str(str_bytes: bytes) -> str:
    return str_bytes.decode("utf-8")

def bytes_to_int(int_bytes: bytes) -> int:
    return int.from_bytes(int_bytes, byteorder="big", signed=False)
