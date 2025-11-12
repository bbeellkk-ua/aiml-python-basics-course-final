from collections import defaultdict
from datetime import datetime
from functools import wraps

from address_book import Record, AddressBook
from note_book import NoteBook


def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except KeyError as e:
            message = str(e) if str(e) else "Contact not found."
            return message

        except ValueError as e:
            message = str(e) if str(e) else "Invalid input."
            return message

        except IndexError as e:
            return str(e) if str(e) else "Not enough arguments."

    return wrapper


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Usage: add [name] [phone]")

    name, phone, *_ = args

    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)

    return message


@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: phone [name]")

    name, *_ = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if not record.phones:
        return f"{name} has no phones."

    return ", ".join(phone.value for phone in record.phones)


@input_error
def change_phone(args, book: AddressBook):
    if len(args) < 3:
        raise IndexError("Usage: change [name] [old_phone] [new_phone]")

    name, old_phone, new_phone, *_ = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."

    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Usage: add-birthday [name] [DD.MM.YYYY]")

    name, birthday_str, *_ = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_birthday(birthday_str)
    return "Birthday set."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: show-birthday [name]")

    name, *_ = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if record.birthday is None:
        return "No birthday set."

    return f"{name}: {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No birthdays next week."

    grouped = defaultdict(list)
    for item in upcoming:
        date_str = item["congratulation_date"].strftime("%d.%m.%Y")
        grouped[date_str].append(item["name"])

    def _to_date(d):
        return datetime.strptime(d, "%d.%m.%Y").date()

    lines = []
    for day in sorted(grouped.keys(), key=_to_date):
        names = ", ".join(grouped[day])
        lines.append(f"{day}: {names}")

    return "\n".join(lines)


@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Usage: add-address [name] [address]")

    name, *address_list = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    record.add_address(" ".join(address_list))
    return "Address set."


@input_error
def show_address(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: show-address [name]")

    name, *_ = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if record.address is None:
        return "No address set."

    return f"{name}: {record.address}"

@input_error
def add_note(args, book: NoteBook):
    if len(args) < 1:
        raise IndexError("Usage: add-note [text]")
    text = " ".join(args).strip()
    if not text:
        raise ValueError("Note text cannot be empty.")
    note = book.add_note(text)
    return f"Note added with id {note.id.value}."


@input_error
def show_notes(book: NoteBook):
    notes = book.get_notes()
    if not notes:
        return "No notes found."
    return "\n".join(str(n) for n in notes)


@input_error
def edit_note(args, book: NoteBook):
    if len(args) < 2:
        raise IndexError("Usage: edit-note [id] [new text]")
    try:
        note_id = int(args[0])
    except ValueError:
        raise ValueError("Note id must be an integer.")
    new_text = " ".join(args[1:]).strip()
    if not new_text:
        raise ValueError("Note cannot be empty.")
    book.edit_note(note_id, new_text)
    return "Note updated."


@input_error
def delete_note(args, book: NoteBook):
    if len(args) < 1:
        raise IndexError("Usage: delete-note [id]")
    try:
        note_id = int(args[0])
    except ValueError:
        raise ValueError("Note id must be an integer.")
    book.delete_note(note_id)
    return "Note deleted."
