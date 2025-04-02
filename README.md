# Contact Assistant Bot

A simple command-line assistant bot that helps manage a personal address book.  
Supports adding, updating, deleting contacts, managing phone numbers and birthdays, and tracks upcoming birthdays.  
All data is persisted between sessions using serialization with `pickle`.

## Features

- Add new contacts with phone numbers and optional birthday
- Edit or remove phone numbers from contacts
- Store and display birthdays in `DD.MM.YYYY` format
- Show all saved contacts
- Display upcoming birthdays for the next 7 days
- Search for phones or birthdays by contact name
- Automatically saves and loads data between runs

## Technologies Used

- Python 3.12.7
- Object-Oriented Programming
- File I/O and `pickle` for data persistence

## File Structure

- `addressbook.py` – Contains data model: `Field`, `Name`, `Phone`, `Birthday`, `Record`, and `AddressBook`
- `bot.py` – Implements the command-line interface and command handlers
- `storage.py` – Handles saving/loading AddressBook with pickle
- `addressbook.pkl` – Binary file used to store persistent contact data
