import os, hashlib
from datetime import datetime
from cryptography.fernet import Fernet
import customtkinter as ctk
from tkinter import messagebox
from tkinter import simpledialog, messagebox

# Files & Encryption Setup
MASTER_FILE = "master.key"
KEY_FILE = "key.key"
VAULT_FILE = "saved_Passwords.txt"

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f: f.write(key)
    with open(KEY_FILE, "rb") as f: return Fernet(f.read())

fernet = load_or_create_key()

# Master Password Check/Set
from tkinter import simpledialog, messagebox

def check_or_set_master():
    if not os.path.exists(MASTER_FILE):
        pw = simpledialog.askstring("Set Master Password", "Enter new master password:", show="*")
        if not pw:
            messagebox.showerror("Error", "Password cannot be empty.")
            exit()
        pw2 = simpledialog.askstring("Confirm Password", "Confirm master password:", show="*")
        if pw != pw2:
            messagebox.showerror("Error", "Passwords don't match.")
            exit()
        with open(MASTER_FILE, "w") as f:
            f.write(hash_password(pw))
    else:
        for _ in range(3):
            pw = simpledialog.askstring("Login", "Enter master password:", show="*")
            with open(MASTER_FILE) as f:
                saved_hash = f.read().strip()
            if pw and hash_password(pw) == saved_hash:
                return
            messagebox.showwarning("Warning", "Incorrect master password!")
        messagebox.showerror("Error", "Too many failed attempts.")
        exit()


# GUI Class
class VaultApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(" Password Vault")
        self.geometry("500x500")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # Inputs
        self.site_entry = ctk.CTkEntry(self, placeholder_text="Site")
        self.site_entry.pack(pady=10)
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.pass_entry.pack(pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self); btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Save", command=self.save_password).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="View All", command=self.view_passwords).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Find", command=self.find_password).grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Delete", command=self.delete_password).grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(self, text="Exit", fg_color="red", command=self.destroy).pack(pady=10)

        # Output Box
        self.output_box = ctk.CTkTextbox(self, width=480, height=200)
        self.output_box.pack(pady=10)

    def save_password(self):
        site = self.site_entry.get().strip()
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()
        if not (site and user and pw):
            messagebox.showerror("Error", "Fill all fields!")
            return
        enc_pw = fernet.encrypt(pw.encode()).decode()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(VAULT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{site}|{user}|{enc_pw}|{ts}\n")
        self.output_box.insert("end", f" Saved: {site}\n")
        self.clear_entries()

    def view_passwords(self):
        self.output_box.delete("1.0", "end")
        if not os.path.exists(VAULT_FILE):
            return
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                parts = line.strip().split("|")
                if len(parts) == 4:
                    self.output_box.insert("end", f"{idx}. {parts[0]} | {parts[1]} | [hidden] | {parts[3]}\n")

    def find_password(self):
        
        target = self.site_entry.get().strip().lower()
        self.output_box.delete("1.0", "end")
        found = False
        if not os.path.exists(VAULT_FILE):
            return
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 4 and parts[0].lower() == target:
                    try:
                        dec = fernet.decrypt(parts[2].encode()).decode()
                        self.output_box.insert("end", f"{parts[0]} | {parts[1]} | {dec} | {parts[3]}\n")
                        found = True
                    except Exception:
                        self.output_box.insert("end", f"{parts[0]} | [Decryption Error: Wrong Key or Corrupt Data]\n")
                        found = True
        if not found:
            self.output_box.insert("end", "No matches found.\n")

    def delete_password(self):
        site = self.site_entry.get().strip().lower()
        user = self.user_entry.get().strip().lower()
        if not os.path.exists(VAULT_FILE):
            self.output_box.insert("end", "No match found.\n")
            return
        deleted = False
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(VAULT_FILE, "w", encoding="utf-8") as f:
            for line in lines:
                p = line.strip().split("|")
                if len(p) == 4 and p[0].lower() == site and p[1].lower() == user:
                    deleted = True
                else:
                    f.write(line)
        self.output_box.insert("end", "✅ Deleted.\n" if deleted else "No match found.\n")
        self.clear_entries()

    def clear_entries(self):
        self.site_entry.delete(0, "end")
        self.user_entry.delete(0, "end")
        self.pass_entry.delete(0, "end")

# App launch
if __name__ == "__main__":
    check_or_set_master()
    app = VaultApp()
    app.mainloop()
