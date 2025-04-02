"""
Command-line assistant bot that interacts with the user and manages contacts via AddressBook.
Supports adding, editing, deleting contacts, phone numbers, and birthdays with validation and error handling.
"""

from functools import wraps
from addressbook import AddressBook, Record, Phone  # Імпортуємо необхідні нам класи з адресної книги
from storage import load_data, save_data            # Імпортуємо функції для збереження та завантаження даних


# Декоратор для обробки помилок.
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "No such contact in your list."
        except Exception as e:
            return f"Error: {e}"
    return inner


# Основний функціонал бота
def parse_input(user_input):
    if not user_input.strip(): return "", []
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide both name and phone.")
    name, phone = args[0], args[1]
    birthday = args[2] if len(args) >= 3 else None
    validated_phone = Phone(phone)
    record = book.find(name)
    message = "Contact updated."
    if not isinstance(record, Record):
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(validated_phone.value)
    if birthday:
        record.add_birthday(birthday)
    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Please provide name, old phone and new phone.")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        return record.edit_phone(old_phone, new_phone)
    return f"No contact with the name {name} found."


@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please provide name.")
    name, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"
    return f"No contact with the name {name} found."


@input_error
def show_all(book: AddressBook):
    if not book: 
        return "No contacts in your list."
    return '\n'.join([f"{name}: {record}" for name, record in book.data.items()])


@input_error
def delete_phone(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide name and phone to delete.")
    name, phone = args[0], args[1]
    record = book.find(name)
    if isinstance(record, Record):
        return record.remove_phone(phone)
    return f"No contact with the name {name} found."


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please provide the name of the contact to delete.")
    name = args[0]
    return book.delete(name)


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Please provide name and birthday. Use DD.MM.YYYY")
    name, birthday, *_ = args
    record = book.find(name)
    if isinstance(record, Record):
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    return f"No contact with the name {name} found."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please provide name.")
    name, *_ = args
    record = book.find(name)
    if isinstance(record, Record) and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return f"No birthday found for {name}."


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming])


@input_error
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if not command: continue
        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "delete-phone":
            print(delete_phone(args, book))
        elif command == "delete-contact":
            print(delete_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()