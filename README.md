# Password---Manager
Python-basierter Passwort-Tresor mit Fernet-Verschlüsselung. Ein Pre-School Projekt zur Demonstration von Logik und Sicherheit.

Passwort-Manager (Python)

Dieses Projekt ist ein Python-basierter Passwort-Tresor, den ich als Eigeninitiative vor dem offiziellen
Start meiner Umschulung zum Fachinformatiker für Anwendungsentwicklung (Juni 2025) entwickelt habe. 
Es dient als praktischer Beleg für mein frühes Interesse an Softwareentwicklung, Datensicherheit und Logiktraining.


Über das Projekt

Ziel des Projekts war es, eine lokale Anwendung zu schaffen, die sensible Zugangsdaten nicht nur speichert, 
sondern durch moderne Verschlüsselungsverfahren absichert. Dabei lag der Fokus auf der praktischen Anwendung 
von File I/O, Hashing und symmetrischer Verschlüsselung.


Funktionen
Master-Passwort-Schutz: Sicherer Zugang zur Anwendung durch ein gehashtes Master-Passwort.

Sichere Verschlüsselung: Alle gespeicherten Passwörter werden mit dem Fernet-Verfahren (Symmetrische Verschlüsselung) gesichert.

Datenmanagement: Vollständige CRUD-Funktionalität (Create, Read, Update, Delete) für Passwörter über eine Konsolenschnittstelle.

Suchfunktion: Schnelles Auffinden von Zugangsdaten anhand des Seitennamens.

Timestamping: Automatische Erfassung des Erstellungsdatums für jeden Eintrag.


Sicherheitsmerkmale
SHA-256 Hashing: Das Master-Passwort wird nicht im Klartext, sondern als SHA-256 Hash gespeichert,
um die Integrität beim Login zu prüfen.

Fernet (cryptography): Nutzung der cryptography-Bibliothek, um sicherzustellen, dass die Passwörter in der Datei saved_Passwords.txt
ohne den geheimen Schlüssel unlesbar sind.


Technologien & Tools

Sprache: Python 3.x 

Bibliotheken: os, hashlib, getpass, cryptography (Fernet), datetime.

Methodik: Modularer Aufbau durch Python-Funktionen und strukturierte Fehlerbehandlung (try-except).

Einfach exe Datei ofnen

oder 👇

Installation & Nutzung
Repository klonen:

Bash
git clone https://github.com/DeinNutzername/Password-Vault.git
Abhängigkeiten installieren:

Bash
pip install cryptography
Programm starten:

Bash
python password_vault.py


Hinweis zur Entwicklung
Dieses Projekt entstand im Selbststudium und markiert den Beginn meiner Reise in die professionelle Anwendungsentwicklung. 
Es spiegelt meine Motivation wider, komplexe technologische Systematiken eigeninitiativ zu durchdringen.
