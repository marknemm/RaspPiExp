from machine import Pin, I2C
from utime import sleep_ms

class LCD():
	""" An LCD screen that displays up to `2 rows` of data, each with up to `16 characters`. """

	def __init__(self, sda_pin_id: int, scl_pin_id: int, addr = None, blen = 1):
		"""
		Args:
			sda_pin_id: The ID of the SDA Pin.
			scl_pin_id: The ID of the SCL Pin.
			addr: The optional initial memory (byte) address to scan. Defaults to `None` for automatic.
			blen: Defaults to `1`.
		"""
		sda = Pin(sda_pin_id)
		scl = Pin(scl_pin_id)
		self.bus = I2C(1, sda=sda, scl=scl, freq=400000)
		self.addr = self.scan_address(addr)
		self.blen = blen
		self.__cursor_addr = 0x80
		self.__buffer = [[0] * 16, [0] * 16]

		self.send_command(0x33) # Must initialize to 8-line mode at first
		sleep_ms(5)
		self.send_command(0x32) # Then initialize to 4-line mode
		sleep_ms(5)
		self.send_command(0x28) # 2 Lines & 5*7 dots
		sleep_ms(5)
		self.send_command(0x0C) # Enable display without cursor
		sleep_ms(5)

		self.clear()
		self.open_light()

	def __del__(self):
		self.clear()

	def __str__(self):
		text = ''

		for line in range(0, 2):
			if line == 1 and self.__buffer[line][0]:
				text += "\n"

			for unicode in self.__buffer[line]:
				if not unicode:
					break
				text += chr(unicode)

		return text

	@property
	def buffer(self) -> list[list[int]]:
		return [buffer_line[:] for buffer_line in self.__buffer] # Copy buffer so immutable.

	@property
	def cursor(self) -> tuple[int, int]:
		row = int(self.__cursor_addr / 0xC0)
		col = self.__cursor_addr - (row * 0x40) - 0x80
		return (row, col)

	def scan_address(self, addr):
		devices = self.bus.scan()

		if devices and addr is not None:
			if addr in devices:
				return addr
			raise Exception(f"LCD at 0x{addr:2X} not found")

		if 0x27 in devices:
			return 0x27
		if 0x3F in devices:
			return 0x3F

		raise Exception("No LCD found")

	def __write_word(self, data: int):
		if self.blen == 1:
			data |= 0x08
		else:
			data &= 0xF7

		word = bytes([data])
		self.bus.writeto(self.addr, word)

	def send_command(self, cmd: int):
		# Send bit7-4 firstly
		buf = cmd & 0xF0
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.__write_word(buf)
		sleep_ms(2)
		buf &= 0xFB               # Make EN = 0
		self.__write_word(buf)

		# Send bit3-0 secondly
		buf = (cmd & 0x0F) << 4
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.__write_word(buf)
		sleep_ms(2)
		buf &= 0xFB               # Make EN = 0
		self.__write_word(buf)

		if cmd >= 0x80:
			self.__cursor_addr = cmd
		elif cmd == 0x01:
			self.__buffer = [[0] * 16, [0] * 16]
			self.__cursor_addr = 0x80

	def send_data(self, data: int):
		(row, col) = self.cursor
		if self.__buffer[row][col] == data:
			self.move_cursor(row, col + 1)
			return # Do not send data if already displaying at cursor location.
		self.__buffer[row][col] = data

		# Send bit7-4 firstly
		buf = data & 0xF0
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.__write_word(buf)
		sleep_ms(2)
		buf &= 0xFB               # Make EN = 0
		self.__write_word(buf)

		# Send bit3-0 secondly
		buf = (data & 0x0F) << 4
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.__write_word(buf)
		sleep_ms(2)
		buf &= 0xFB               # Make EN = 0
		self.__write_word(buf)

		self.__cursor_addr += 1

	def clear(self):
		self.send_command(0x01) # Clear Screen

	def open_light(self):  # Enable the backlight
		self.bus.writeto(self.addr, bytes([0x08]))

	def write(self, x: int, y: int, string: str):
		self.move_cursor(x, y)

		for char in string:
			self.send_data(ord(char))

	def move_cursor(self, x: int, y: int):
		if x < 0:
			x = 0
		if x > 15:
			x = 15
		if y < 0:
			y = 0
		if y > 1:
			y = 1

		self.send_command(0x80 + 0x40 * y + x)

	def message(self, text: str, no_clear = False):
		if str(self) == text:
			return # Do not process message if already displaying it.

		if not no_clear:
			self.clear()

		for char in text:
			if char == '\n':
				self.send_command(0xC0) # next line
			else:
				self.send_data(ord(char))
