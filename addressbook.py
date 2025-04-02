"""
AddressBook module with classes for managing contacts, phone numbers, and birthdays.
Supports validation, record manipulation, and upcoming birthday tracking.
"""

from collections import UserDict
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Field:
    value: str
    def __str__(self):
        return str(self.value)


@dataclass
class Name(Field):
    pass


@dataclass
class Phone(Field):
    def __post_init__(self):
        self.validate(self.value)

    def validate(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")


@dataclass
class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


@dataclass
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        parts = [f"Contact name: {self.name.value}"]
        if self.phones:
            parts.append(f"phones: {'; '.join(p.value for p in self.phones)}")
        if self.birthday:
            parts.append(f"birthday: {self.birthday.value.strftime('%d.%m.%Y')}")
        return ", ".join(parts)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone: str):
        try:
            self.phones.remove(Phone(phone))
            return f"Phone {phone} was removed from contact {self.name.value}."
        except ValueError:
            return f"Phone {phone} not found in contact {self.name.value}."

    def edit_phone(self, old_phone: str, new_phone: str):
        for idx, p in enumerate(self.phones): 
            if p == Phone(old_phone):
                self.phones[idx] = Phone(new_phone)
                return f"Phone {old_phone} was updated to {new_phone} for contact {self.name.value}."
        return f"Phone {old_phone} not found in contact {self.name.value}."

    def find_phone(self, phone: str):
        if Phone(phone) in self.phones:
            return f"{self.name.value}: {phone}"
        return f"Phone {phone} not found for contact {self.name.value}."
    
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} has been deleted."
        return f"No contact with the name {name} was found."
    
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                days_to_birthday = (birthday_this_year - today).days
                if 0 <= days_to_birthday <= 7:
                    if birthday_this_year.weekday() in [5, 6]:
                        days_to_shift = 7 - birthday_this_year.weekday()
                        birthday_this_year += timedelta(days=days_to_shift)
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": birthday_this_year.strftime('%d.%m.%Y')
                    })
        return upcoming_birthdays