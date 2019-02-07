import sys
from color import *

# -------------- FUTURE CLASS IMPLEMENTATIONS ------------------

class Integer:
	def __init__(self, value):
		assert value.isnumeric
		self.value = int(value)
		pass

class String:
	def __init__(self, string):
		self.string = string
		pass

class Bool:
	def __init__(self, value):
		self.value = value
		pass

class Double:
	def __init__(self, value):
		self.value = value
		pass

class List:
	def __init__(self):
		self.list = []
		pass

class Dictionary:
	def __init__(self):
		self.dict = {}
		pass

# ----------------- VARIABLE STUFF -------------------------

class Variable:

	def __init__(self, var_type, name, content):
		self.type = var_type
		self.name = name
		self.content = content

def store_var(line):

	rhs_var = get_var(line[3])
	declare_type = line[0]

	if rhs_var:
		value = rhs_var.content
		if line[0] == "int":
			assert (rhs_var.type == "int")
	else:
		value = line[3]
		if declare_type == "int":
			value = int(value)
		elif declare_type == "bool":
			if value == "True" or value == "true":
				value = True
			elif value == "False" or value == "false":
				value = False
			else:
				print(con_color.FAIL, "%s is not a correct assignment for type bool" % value, con_color.ENDC)
				return
		elif declare_type == "string":
			value = str(line[3])
			assert value[0] == '\"' and value[len(value) - 1] == '\"'
			value.replace("\"", "")

	if line[2] != "=":
		print(con_color.FAIL, "You must assign a value upon declaration", con_color.ENDC)
		return False
	else:
		var = Variable(line[0], line[1], value)
		v_manager.append(var)

	return True

def print_var(line):
	if get_var(line[1]):
		print(get_var(line[1]).content)
	else:
		print(line[1])

def get_var(search_name):
	for var in v_manager.vars:
		if var.name == search_name:
			return var
	return
	# print(con_color.FAIL, "Input var '%s' does not exist.." % search_name, con_color.ENDC)
	# quit()

def set_var(var_to_set):
	for var in v_manager.vars:
		if var.name == var_to_set.name:
			var.content = var_to_set.content
			return
	# print(var_to_set.name)
	print(con_color.FAIL, "Input var '%s' does not exist.." % var_to_set.name, con_color.ENDC)
	quit()

# --------------------- ASSIGNMENT ----------------------------

def assign(current_line):
	print(current_line)
	assert(len(current_line) == 4)
	assert(current_line[2] == "=")
	value = current_line[3]
	lhs_var = get_var(current_line[1])
	rhs_var = get_var(value)
	if rhs_var:  # if we are assigning one var to another
		assert(lhs_var.type == rhs_var.type)
		lhs_var.content = rhs_var.content
	else:  # if we are assigning a raw value such as int, bool, string ....
		if lhs_var.type == "int":
			if type(value) != int:
				assert (value.isnumeric())
				lhs_var.content = int(value)
			else:
				lhs_var.content = value
		if lhs_var.type == "bool":
			if value == "True" or value == "true":
				lhs_var.content = True
			elif value == "False" or value == "false":
				lhs_var.content = False

	# push = content change to the Var Manager
	set_var(lhs_var)

# ------------------------- CALCULATION ---------------------------------

def calculate(current_line):

	# TODO: ALLOW FOR EXPRESSIONS LIKE a + 1 (var + literal)
	# 		ADD STRING CALCULATIONS

	lhs = get_var(current_line[1])
	operation = current_line[2]
	rhs = get_var(current_line[3])

	if not lhs:
		print("woah!")
	if not rhs:
		print("wowee!")

	assert(lhs.type == rhs.type)

	if lhs.type == "int":
		a = int(lhs.content)
		b = int(rhs.content)

		if operation == "+":
			# print(a + b)
			return a + b
		elif operation == "-":
			# print(a - b)
			return a - b
		elif operation == "*":
			# print(a * b)
			return a * b
		elif operation == "/":
			# print(a / b)
			return a / b
	elif lhs.type == "bool":
		a = lhs.content
		b = rhs.content

		if operation == "and":
			# print(a and b)
			return a and b
		elif operation == "or":
			# print(a or b)
			return a or b
	elif lhs.type == "str":
		a = lhs.content
		b = rhs.content

def make_object(line):
	pass

def make_if(line):
	pass

def make_else(line):
	pass

def do_return(line):
	pass

# ---------------------------- COMMANDER --------------------------------

class Commander:

	def __init__(self):
		self.command_list = ["int", "bool", "string", "assign", "calc", "object", "if", "else", "return", "print"]

	def command(self, current_line):

		# we need a function call stack!!
		# utilize getattr(sys.modules[__name__], "call_%s" % fieldname)()
		# where call_%s % fieldname() will concatenate to call_fieldname()

		index = 0

		for i in range(len(current_line)):
			# if i in self.command_list:
				# call_stack.push(i)
				# index = index
			if current_line[i] in self.command_list:
				call_stack.push(current_line[i])
				index = i

		while call_stack.size() != 0:

			func = call_stack.pop()

			sub_line = current_line[index:]

			if func == "int" or func == "bool" or func == "string":
				store_var(sub_line)
				current_line.remove(func)
			elif func == "assign":
				assign(sub_line)
				current_line.remove(func)
			elif func == "calc":
				result = calculate(sub_line)
				del current_line[index:]
				current_line.append(result)
			elif func == "object":
				make_object(sub_line)
				current_line.remove(func)
			elif func == "if":
				make_if(sub_line)
				current_line.remove(func)
			elif func == "else":
				make_else(sub_line)
				current_line.remove(func)
			elif func == "return":
				do_return(sub_line)
				current_line.remove(func)
			elif func == "print":
				print_var(sub_line)
				current_line.remove(func)
			else:
				print(con_color.FAIL, func, "is not a known term...", con_color.ENDC)
				return False

			# now, look back through line for more commands
			# store index as that

			for i in range(len(current_line)):
				if current_line[i] in self.command_list:
					index = i

# --------------------------- VAR MANAGER -------------------------

class VarManager:

	def __init__(self):
		self.vars = []

	def append(self, var):
		self.vars.append(var)

	def print_vars(self):
		for var in self.vars:
			print(var.name, var.content)

	def var_lookup(self, search_var):
		for var in self.vars:
			if var.name == search_var:
				return var

# -------------------- OBJECT STUFF ------------------------

class UserObject:

	def __init__(self, name):
		self.name = name
		self.object_var_dict = {}

	def set_object_vars(self):
		pass

class ObjectManager:

	def __init__(self):
		self.objects = []

	def push_object(self, u_object):
		self.objects.append(u_object)

# ---------------------- PROCESS MANAGER -----------------------

class ProcessManagerStack:

	def __init__(self):
		self.call_stack = []

	def is_empty(self):
		return self.call_stack == []

	def push(self, item):
		self.call_stack.append(item)

	def pop(self):

		return self.call_stack.pop()

	def peek(self):
		return self.call_stack[len(self.call_stack) - 1]

	def size(self):
		return len(self.call_stack)

# -------------------- PARSER ----------------------------

def parse(u_input):

	line = u_input.split()

	commander.command(line)

	# check for proper format

	for i in range(len(line)):
		if i == 0 and line[i] == "and":
			print(con_color.FAIL, line[i], "needs a variable on both ends", con_color.ENDC)
			return False
		elif i == 0 and line[i] == "or":
			print(con_color.FAIL, i, "needs a variable on both ends", con_color.ENDC)
			return False
		elif i == len(line) - 1 and line[i] == "and":
			print(con_color.FAIL, line[i], "needs a variable on both ends", con_color.ENDC)
			return False
		elif i == len(line) - 1 and line[i] == "or":
			print(con_color.FAIL, line[i], "needs a variable on both ends", con_color.ENDC)
			return False

	return True

# --------------------- MAIN STUFF -----------------------

v_manager = VarManager()
commander = Commander()
call_stack = ProcessManagerStack()

print("__Logic Calculator__\n")

con_color = color()

line_counter = 0

if len(sys.argv) > 1:
	print(str(sys.argv))

while True:
	line_counter = line_counter + 1
	counter_string = str(line_counter)

	# take commands
	command = input("%s::>> " % counter_string)

	# parse the line
	if command == "quit" or command == "q":
		# v_manager.print_vars()
		break
	elif command == "run":
		# run through logic (use the stacker, make sure this has been stacked previously during parsing)
		print("running...")
		pass
	else:
		if parse(command):  # format correct
			# print(con_color.OKGREEN + "Good" + con_color.ENDC)
			pass
		else:
			print(con_color.FAIL + "Something went wrong..." + con_color.ENDC)
