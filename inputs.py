import curses
import os

# ================================================================== #
# License and Credit
# author   - Silas Harvey
# licence  - GNU General Public License v3.0
# ================================================================== #

# ================================================================== #
# Custom Class Declaration
# init     - accepts parent class as only argument
# hint     - returns a list of content based on current value
# validate - checks the current value before submission
# ================================================================== #

# ================================================================== #
# Included Types Of Input
# basic    - simple editable string
# path     - filepath with hints and validation
# ================================================================== #

class basic:
	def __init__(self, parent):
		self.parent = parent

	def hint(self):
		return []

	def validate(self):
		return True


class path:
	def __init__(self, parent):
		self.parent = parent
		os.chdir(self.parent.default)

	def hint(self):
		path = self.parent.default

		if os.path.isdir(path) and path.rstrip("/") != os.getcwd():
			os.chdir(path)

		flist = os.listdir(os.getcwd())

		for i in flist[:]:
			if i.startswith(".") or (path.replace(os.getcwd(), "") != "" and path.replace(os.getcwd(), "").strip("/") not in i):
				flist.remove(i)
				self.parent.line = 0

		return flist

	def validate(self):
		return os.path.exists(self.parent.default)





# ================================================================== #
# Main Class
# initilise class with title and default
# main loop contains the curses code to display a common interface
# interface includes set keybindings for navigation
# ================================================================== #

class capture_class:
	def __init__(self, title, default):
		self.title = title
		self.default = default
		self.line = 0
		self.cursor = 0

		self.screen = curses.initscr() 
		self.screen.keypad(1)
		curses.cbreak()
		curses.curs_set(0)
		curses.start_color()

	def main(self, typ):
		while True:
			# Put title and current value on buffer
			self.screen.clear()
			self.screen.addstr(self.title + "\n"*2)
			self.screen.addstr(self.default[:len(self.default)-self.cursor-1])
			self.screen.addch(self.default[len(self.default)-self.cursor-1], curses.A_REVERSE)
			self.screen.addstr(self.default[len(self.default)-self.cursor:])

			# Write hint below current value: e.g. directories available
			c = self.screen.getyx()
			height = self.screen.getmaxyx()[0] - 5
			slist = typ.hint()
			self.screen.addstr("\n")
			for i in slist[self.line:self.line+height]:
				self.screen.addstr("\n" + i)
			self.screen.move(*c)

			# Keyboard Hooks
			char = self.screen.getch()
			if char == curses.KEY_BACKSPACE:
				self.default = self.default[:len(self.default)-self.cursor-1] + self.default[len(self.default)-self.cursor:]
			elif char == curses.KEY_UP and self.line > 0:
				self.line -= 1
			elif char == curses.KEY_DOWN and self.line+height < len(slist):
				self.line += 1
			elif char == curses.KEY_LEFT and self.cursor < len(self.default):
				self.cursor += 1
			elif char == curses.KEY_RIGHT and self.cursor > 0:
				self.cursor -= 1
			elif char in [curses.KEY_ENTER, 10, 13]:
				if typ.validate():
					curses.endwin()
					return self.default
			elif char < 256 :
				self.default = self.default[:len(self.default)-self.cursor] + chr(char) + self.default[len(self.default)-self.cursor:]

			# Refresh screen with buffer contents
			self.screen.refresh()





# ================================================================== #
# Wrapper Function
# wraps capture_class and the inputtype classes into a function
# takes 3 optional arguments
# creates instance of capture_class with 2 arguments
# creates an intype instance and passes the capture_class instance
# returns the result of capture_class's main method
# catches and reraises all errors after terminating curses
# ================================================================== #

def capture(title="", default="", intype=basic):
	try:
		instance = capture_class(title, default)
		input_type = intype(instance)
		return instance.main(input_type)
	except:
		curses.endwin()
		raise