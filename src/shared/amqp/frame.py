class FrameHeader:
    __slots__ = ["size", "data_offset", "type", "channel"]
    def __init__(self, size: int, data_offset: int, frame_type: int, channel: int) -> None:
        self.size: int = size
        self.data_offset: int = data_offset
        self.type: int = frame_type
        self.channel: int = channel

    def to_bytes(self) -> bytes:
        pass
