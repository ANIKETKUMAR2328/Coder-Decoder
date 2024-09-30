import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import string

# Function to generate a random key
def generate_key():
    characters = string.ascii_letters + string.digits + string.punctuation
    shuffled = list(characters)
    random.shuffle(shuffled)
    return dict(zip(characters, shuffled))

# Function to encrypt a message using a given key
def encrypt_message(message, key):
    encrypted_message = ''.join(key.get(char, char) for char in message)
    return encrypted_message

# Function to decrypt a message using a given key
def decrypt_message(encrypted_message, key):
    reversed_key = {v: k for k, v in key.items()}
    decrypted_message = ''.join(reversed_key.get(char, char) for char in encrypted_message)
    return decrypted_message

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Encrypted Chat")

        self.text_area = tk.Text(self.root, height=20, width=50)
        self.text_area.pack()

        self.entry_field = tk.Entry(self.root, width=50)
        self.entry_field.pack()
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.keys = {}
        self.encrypted_messages = {}
        self.message_id = 0

    def send_message(self, event=None):
        message = self.entry_field.get()
        if message:
            key = generate_key()
            encrypted_message = encrypt_message(message, key)
            self.message_id += 1
            self.keys[self.message_id] = key
            self.encrypted_messages[self.message_id] = encrypted_message

            self.text_area.insert(tk.END, f"You (Encrypted): {encrypted_message}\n")
            self.text_area.insert(tk.END, f"Key ID: {self.message_id}\n")

            self.entry_field.delete(0, tk.END)

    def decrypt_message_prompt(self):
        if not self.keys:
            messagebox.showinfo("No Messages", "There are no messages to decrypt.")
            return

        key_id = simpledialog.askinteger("Decrypt", "Enter the key ID:")
        if key_id in self.keys:
            key = self.keys[key_id]
            encrypted_message = self.encrypted_messages[key_id]
            decrypted_message = decrypt_message(encrypted_message, key)
            messagebox.showinfo("Decrypted Message", f"Decrypted Message: {decrypted_message}")
        else:
            messagebox.showerror("Error", "Invalid key ID.")

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Options", menu=file_menu)
        file_menu.add_command(label="Decrypt Message", command=self.decrypt_message_prompt)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

def main():
    root = tk.Tk()
    chat_window = ChatWindow(root)
    chat_window.create_menu()
    root.mainloop()

if __name__ == "__main__":
    main()
