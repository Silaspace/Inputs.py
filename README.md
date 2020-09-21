# Inputs.py

Inputs.py is a python library designed for UNIX systems that makes use of the curses library to provide more advanced inputs. The curses library allows lower level access to the linux terminal that makes more elegant inputs possible by using hints and allowing raw input.

# Use

To use the libray you have to call the capture method, for example:
```
import inputs
x = inputs.capture()
```

The capture method has three optional arguments:
+ title
+ default
+ intype

The 'title' argument is equivilent to the string passed to python's regular input method, it tells the user what the input wants. For example: `x = inputs.capture("Name")`
would produce an input with "Name" as the title. Its default value is an empty string.

the 'default' argument is the default value that the input starts with. For example, if you wanted a filepath you might want to start in the current working directory. To achieve this, you could call `x = inputs.capture("Path", "/home/pi/projects/") # Or you could use os.getcwd()`. Its default value is an empty string.

Lastly, the 'intype' argument specifies what type of input it should expect. The default value is the basic class, which is the input type for a regular string. These intype classes are explained in more depth in the section below. The other included intype is path, and can be called with `x = inputs.capture("Path", "/home/pi/", inputs.path)`


# Intype Classes

The basic class (which is for a simple string) looks like this.

```
class basic:
	def __init__(self, parent):
		self.parent = parent

	def hint(self):
		return []

	def validate(self):
		return True
```

Intype classes require 3 methods, `__init__`, `hint` and `validate`.
The `__init__` function should always look the same, taking the arguments self and parent, then setting self.parent to the parent argument. This allows the captured data to be accessed in real time for hints or preproccessing.

The `hint` method should always return a list for the input to display. For the inbuilt path intype, the hint method returns a list of files and folders that is narrowed down as the user types. If unused, it should always return an empty list.

The `validate` method returns `True` if the input is valid. For example, the path intype only returns true and allows the input to be accepted when the input is an existing path.

The data from the parent class is accessed through `self.parent.xxxxxx` where `xxxxxx` is one of 4 attributes:
+ default
+ title
+ line
+ cursor

The `title` attribute is the same as the argument passed into the capture function and is stored unchaging. The `default` attribute is the current value of the user's text input, which changes on every keypress. This is most useful when creating the hint or validate methods.

The `line` attribute stores the postion of the scolling hints field and is largly useless outside the parent class. Similarly, the `cursor` attribute stores the postion of the cursor in the text field and is mostly used inside the parent function.
