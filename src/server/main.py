import sys
import asyncio
from typing import Any

def get_event_loop() -> Any:
	if sys.platform.startswith("win"):
		loop = asyncio.ProactorEventLoop()
		asyncio.set_event_loop(loop)
	else:
		loop = asyncio.get_event_loop()

	return loop

class Server:
	def __init__(self) -> None:
		self.loop = get_event_loop()

if __name__ == "__main__":
	server = Server()
