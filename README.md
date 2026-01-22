
* *
    P A S S W O R D   M A N A G E R               *
* *

Author: Georgios Karakatsanis
Location: Bietigheim-Bissingen, Germany
Date: January 2026

=== [ 01. INTRODUCTION ] ======================================================

This project is a standalone password management system developed in Python. 
I built this independently prior to starting my formal IT training in 2025. 
The goal was to move beyond theory and implement a functional tool that 
demonstrates my technical transition from a Special Forces Officer to an 
Application Developer[cite: 54, 105].

=== [ 02. TECHNICAL SPECIFICATIONS ] ==========================================

The application utilizes the following security protocols:

* HASHING: SHA-256 (via hashlib) for master password validation.
* ENCRYPTION: Fernet symmetric encryption (via cryptography library) for
  stored credentials.
* DATA STORAGE: Local file system (saved_Passwords.txt).
* ARCHITECTURE: Modular functions with a dedicated GUI class (OOP) for the
  visual version.

=== [ 03. CORE FEATURES ] =====================================================

- Master password authentication with 3-attempt lockout.
- Encrypted storage of Site, Username, and Password.
- Search-by-site functionality.
- Automated timestamping for entry tracking.
- Secure terminal input using 'getpass' for the CLI version.

=== [ 04. INSTALLATION & USAGE ] ==============================================

Dependencies:
$ pip install cryptography customtkinter

Execution:
$ python vault_gui.py   (for the GUI version)
$ python vault_cli.py   (for the terminal version)

Note: Standalone .exe binaries are available in the "Releases" section.

=== [ 05. DEVELOPER NOTES ] ===================================================

I am fascinated by what happens "under the hood" of software. This vault is 
my first deep dive into the internal mechanics of secure data handling.

===============================================================================
[ END OF README ]
