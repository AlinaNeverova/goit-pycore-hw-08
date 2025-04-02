"""
Handles saving and loading AddressBook data to and from disk using the pickle module.
Ensures contact data persists between sessions.
"""

import pickle
from addressbook import AddressBook

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()