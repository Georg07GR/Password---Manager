
#region IMPORT MODULES 

import os
import hashlib
import getpass
from cryptography.fernet import Fernet
from datetime import datetime
# endregion

#region MASTER PASSWORD SETUP & AUTHENTICATION 

try:
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears the console for a fresh start
except Exception:
    pass                                             # Ignores errors if clearing the console fails
print("="*30)
print("   Welcome to Password Vault   ")
print("="*30)

master_file = "master.key"                          # Files the master key
def hash_password(password):                        
    return hashlib.sha256(password.encode()).hexdigest()    # Hashing the password using SHA-256

if not os.path.exists(master_file):
    print("No master Password set. Please set a master Password.")
    while True:                                                         # Loop until a valid master password is set
        pw1 = input("Create a new master Password: ")   #getpass.getpass is used to securely input the password without echoing it
        pw2 = input("Confirm the master Password: ")
        if pw1 != pw2:                                  # Check if the passwords match
            print("Passwords do not match. Please try again.")
        elif not pw1:
            print("Password cannot be empty. Please try again.")
        else:                                            # If passwords match and are not empty, hashes the password and saves it
            with open(master_file, "w") as f:
                f.write(hash_password(pw1))
            print("Master Password set successfully.")
            break
else:
    with open(master_file, "r") as f: 
        saved_hash = f.read().strip()                
    attempts = 3    
    for _ in range(attempts):                          # Gives 3 attempts before locks user out
        pw = input("Enter the master Password: ")
        if hash_password(pw) == saved_hash:
            print("Access granted.")
            break
        else:
            print("Incorrect master Password. Try again.")
    else:
        print("Too many incorrect attempts. Exiting program.")
        exit()
#endregion


#region ENCRYPTION KEY SETUP

key_file_path = "key.key"                               # Path to the file where the encryption key is stored
if not os.path.exists(key_file_path):
    print("Encryption key not found. Generating a new key...")
    key = Fernet.generate_key()                         # Generates and saves a new encryption key
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)
else:
    with open(key_file_path, "rb") as key_file:         # Loads the encryption key from a file
        key = key_file.read()
fernet = Fernet(key)
#endregion


#region PASSWORD VAULT OPERATIONS

vault_file = "saved_Passwords.txt"                       # File where passwords are stored

while True:                                              # Main loop for the password vault operations
      
    option_1 = "[1] Save a new Password"
    option_2 = "[2] View all saved Passwords"
    option_3 = "[3] Find a Password by site"
    option_4 = "[4] Delete a Password"
    option_5 = "[5] Exit"

    print("="*30)
    print("   Password Vault Main Menu   ") 
    print("="*30)
    print("Please choose an option:")
    
    ## Displays the options to the user ##
    print(f"\n{option_1}\n{option_2}\n{option_3}\n{option_4}\n{option_5}")
    print("="*30) 
    try:
        user_press = int(input("Choose an option: "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        continue
#endregion


#region Option 1:
    if user_press == 1:
        print("You choose to: Save a new Password.")
        site_name = input("Site: ").strip()
        if not site_name:
            print("Site name is required. Please try again.")
            continue
        user_name = input("User Name: ").strip()
        if not user_name:
            print("User name is required. Please try again.")
            continue
        password = input("Password: ").strip()
        if not password:
            print("Password is required. Please try again.")
            continue

        # Encrypts the password before saving
        encrypted_password = fernet.encrypt(password.encode()).decode()
        print("Saving your password...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # Get the current timestamp

        # The file is created if it does not exist. Each new entry is appended to the file.
        with open(vault_file, "a", encoding="utf-8") as file:   
            file.write(f"{site_name}|{user_name}|{encrypted_password}|{timestamp}\n")
        print("Saved successfully!")
#endregion

#region Option 2:
    elif user_press == 2:
        print("You choose to: View all saved Passwords.")
        try:
            with open(vault_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("No saved passwords found.")
            lines = []
        if not lines:
            print("No saved passwords found.")
        else:
            print("Saved Passwords:")
            print("------------------------")
            entries = []
            for idx, line in enumerate(lines, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) == 4:
                    site, user, password, timestamp = parts
                    print(f"[{idx}] Site: {site}")
                    print(f"    User Name: {user}")
                    print(f"    Password: [hidden]")
                    print(f"    Saved: {timestamp}")
                    print("------------------------")
                    entries.append((site, user, password, timestamp))
                else:
                    print(f"Warning: Skipping malformed entry: {line}")
            if entries:
                reveal = input("Would you like to reveal a password? (y/n): ").strip().lower()
                if reveal == "y":
                    try:
                        choice = int(input(f"Enter the number (1-{len(entries)}): ")) - 1
                        if 0 <= choice < len(entries):
                            decrypted = fernet.decrypt(entries[choice][2].encode()).decode()
                            print(f"Password for {entries[choice][0]} ({entries[choice][1]}): {decrypted}")
                            print(f"Saved at: {entries[choice][3]}")
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Invalid input.")
#endregion

#region Option 3:
    elif user_press == 3:
        site_to_search = input("Enter site name to search: ").strip().lower()
        matches = []
        try:
            with open(vault_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("No saved passwords found.")
            lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4 and parts[0].lower() == site_to_search:
                matches.append(parts)

        if not matches:
            print("No matching site found.")
        else:
            for i, (site, user, _, timestamp) in enumerate(matches, start=1):
                print(f"[{i}] {site}\n{user}\nSaved: {timestamp}")

            try:     # Error handling to ensure app stability during decryption failures
                choice = int(input(f"Choose a number (1-{len(matches)}): ")) - 1
                if 0 <= choice < len(matches):
                    decrypted = fernet.decrypt(matches[choice][2].encode()).decode()
                    print(f"Password for {matches[choice][0]} ({matches[choice][1]}): {decrypted}")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
#endregion


#region  Option 4:
    elif user_press == 4:
        print("You choose to: Delete a Password.")
        site_to_delete = input("Enter site name: ").strip().lower()

        try:
            with open(vault_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("No passwords found.")
            continue

        matches = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4 and parts[0].lower() == site_to_delete:
                matches.append(parts)

        if not matches:
            print("No matching site found.")
            continue

        print("These entries match your site:")
        for entry in matches:
            site, user, encrypted_password, timestamp = entry
            try:
                decrypted = fernet.decrypt(encrypted_password.encode()).decode()
            except Exception:
                decrypted = "[decryption error]"
            print("------------------------")
            print(f" Site: {site}")
            print(f" User Name: {user}")
            print(f" Password: {decrypted}")
            print(f" Saved: {timestamp}")
            print("------------------------")

        user_delete = input("Enter the username to delete: ").strip().lower()
        deleted = False
        new_lines = []

        for line in lines:
            line_strip = line.strip()
            if not line_strip:
                continue
            parts = line_strip.split("|")
            if len(parts) == 4 and parts[0].lower() == site_to_delete and parts[1].lower() == user_delete:
                deleted = True
                continue  # Skip this entry
            new_lines.append(line_strip + "\n")

        with open(vault_file, "w", encoding="utf-8") as file:
            file.writelines(new_lines)

        if deleted:
            print("Entry deleted successfully.")
        else:
            print("No matching site and username found.")  
#endregion


#region Option 5: 
    elif user_press == 5:
        print("="*30)   
        print("You choose to: Exit the program.")
        print("Thank you for using Password Vault. Goodbye!")
        print("="*30)
        break  # Exit the loop and program 

    ## Invalid option handling ##
    else:
        print("Invalid option. Please choose between 1–5.")