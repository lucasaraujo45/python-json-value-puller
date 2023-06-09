import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                if k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
    if file_path:
        with open(file_path, 'r') as json_file:
            json_obj = json.load(json_file)
        return json_obj
    else:
        return None

def main():
    # Create the main window
    root = tk.Tk()
    root.geometry("400x300")
    root.title("JSON Key Extractor")
    root.configure(bg='lightblue')

    # Create a StringVar() to store the user input
    key_var = tk.StringVar()

    # Create a Label
    key_label = tk.Label(root, text='Enter Key:', bg='lightblue')
    key_label.pack(pady=10)

    # Create a Entry widget
    key_entry = tk.Entry(root, textvariable=key_var)
    key_entry.pack()

    # Create a scrolledtext widget to display the result
    result_box = tk.scrolledtext.ScrolledText(root, width=40, height=10)
    result_box.pack(pady=10)

    def handle_button_click():
        json_obj = open_file()
        if json_obj is not None:
            key = key_var.get()
            values = extract_values(json_obj, key)
            result = ", ".join(str(val) for val in values)
            result_box.delete('1.0', tk.END)
            result_box.insert(tk.END, result)
            root.clipboard_clear()
            root.clipboard_append(result)

    # Create a Button
    button = tk.Button(root, text="Choose JSON File", command=handle_button_click, bg='lightgreen')
    button.pack(pady=10)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
