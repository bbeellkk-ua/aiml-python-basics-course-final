from collections import defaultdict
from datetime import datetime
from functools import wraps

from address_book import Record, AddressBook


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
