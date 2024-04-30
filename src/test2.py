from tkinter import *

# Function to print the selected value
def print_selected_value(*args):
    print("Selected value:", selected_value.get())

# Creating the root window 
root = Tk() 

# Creating a StringVar to store the selected value
selected_value = StringVar(root)

# Trace the changes in selected value
selected_value.trace_add("write", print_selected_value)

# Available options for OptionMenu
options = []
for value in range(100):
    options.append(str(value))

# Setting default value
selected_value.set(options[0])

# Creating the OptionMenu
option_menu = OptionMenu(root, selected_value, *options)
option_menu.pack()

root.mainloop()
