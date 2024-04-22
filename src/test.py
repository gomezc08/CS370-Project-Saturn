import tkinter as tk
def on_option_select():
    selected = selected_option.get()
    result_label.config(text=f"Selected Option: {selected}")
root = tk.Tk()
root.title("Dropdown Menu Example")
root.geometry("400x300")
# Create a StringVar to hold the selected option
selected_option = tk.StringVar()
# Create the dropdown menu
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.pack(pady=10)
# Add a button to display the selected option
show_button = tk.Button(root, text="Show Selection", command=on_option_select)
show_button.pack()
# Label to display the selected option
result_label = tk.Label(root, text="")
result_label.pack()
root.mainloop()