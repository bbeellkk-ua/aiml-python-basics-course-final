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
def change_name(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Usage: change-name [old_name] [new_name]")
    old_name, new_name, *_ = args
    if old_name == new_name:
        raise ValueError("New name must be different.")
    book.rename(old_name, new_name)
    return "Contact renamed."


@input_error
def contacts_markdown(book: AddressBook):
    if not book.data:
        return "No contacts found."

    records = sorted(book.values(), key=lambda r: r.name.value.lower())

    def _esc(s: str) -> str:
        return s.replace("|", "\\|")

    # Build escaped rows
    rows = []
    for r in records:
        name = _esc(r.name.value)
        phones = _esc(", ".join(p.value for p in r.phones) if r.phones else "")
        birthday = _esc(str(r.birthday) if r.birthday else "")
        address = _esc(str(r.address) if r.address else "")
        rows.append([name, phones, birthday, address])

    headers = ["Name", "Phones", "Birthday", "Address"]

    # Calculate max widths per column (including headers)
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if len(cell) > col_widths[i]:
                col_widths[i] = len(cell)

    # Build header row with padding
    header_row = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

    # Build alignment/separator row (left, left, center, left)
    def _align(width, align="left"):
        # produce markdown alignment marker matching width
        if width < 3:
            width = 3
        if align == "center":
            return ":" + "-" * (width - 2) + ":"
        elif align == "right":
            return "-" * (width - 1) + ":"
        else:
            return ":" + "-" * (width - 1)  # left

    alignments = ["left", "left", "center", "left"]
    separator_row = "| " + " | ".join(_align(col_widths[i], alignments[i]) for i in range(len(col_widths))) + " |"

    # Build data rows with padding (center birthday for readability)
    def _pad(cell, width, align="left"):
        if align == "center":
            total = width - len(cell)
            left = total // 2
            right = total - left
            return " " * left + cell + " " * right
        elif align == "right":
            return cell.rjust(width)
        else:
            return cell.ljust(width)

    lines = [header_row, separator_row]
    for row in rows:
        padded = []
        for i, cell in enumerate(row):
            padded.append(_pad(cell, col_widths[i], alignments[i]))
        lines.append("| " + " | ".join(padded) + " |")

    return "\n".join(lines)


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
def birthdays(args, book: AddressBook, default_days: int = 7):
    if args and len(args) > 0:
        try:
            days = int(args[0])
            if days < 1:
                raise ValueError("Number of days must be positive.")
        except ValueError as e:
            if "positive" in str(e):
                raise
            raise ValueError("Number of days must be an integer.")
    else:
        days = default_days

    upcoming = book.get_upcoming_birthdays(days)

    if not upcoming:
        return f"No birthdays in the next {days} days."

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


@input_error
def tag_note(args, book: NoteBook):
    if len(args) < 2:
        raise IndexError("Usage: tag-note [id] [tag1] [tag2] ...")
    try:
        note_id = int(args[0])
    except ValueError:
        raise ValueError("Note id must be an integer.")

    tags = [t.strip() for t in args[1:] if t.strip()]
    if not tags:
        raise ValueError("At least one tag is required.")
    book.add_tags(note_id, tags)
    return "Tags added."


@input_error
def untag_note(args, book: NoteBook):
    if len(args) < 2:
        raise IndexError("Usage: untag-note [id] [tag1] [tag2] ...")
    try:
        note_id = int(args[0])
    except ValueError:
        raise ValueError("Note id must be an integer.")

    tags = [t.strip() for t in args[1:] if t.strip()]
    if not tags:
        raise ValueError("At least one tag is required.")
    book.remove_tags(note_id, tags)
    return "Tags removed."


@input_error
def find_notes(args, book: NoteBook):
    if len(args) < 1:
        raise IndexError("Usage: find-notes [tag1] [tag2] ...")
    tags = [t.strip() for t in args if t.strip()]
    if not tags:
        raise ValueError("At least one tag is required.")

    notes = book.search_by_tags(tags)
    if not notes:
        return "No notes found for given tags."
    return "\n".join(str(n) for n in notes)


@input_error
def sort_notes_by_tags(args, book: NoteBook):
    if args:
        raise ValueError("Usage: sort-notes-by-tags")
    notes = book.sort_by_tags()
    if not notes:
        return "No notes found."
    return "\n".join(str(n) for n in notes)


@input_error
def set_birthdays_days(args, assistant):
    if len(args) < 1:
        raise IndexError("Usage: set-birthdays-days [days]")
    try:
        days = int(args[0])
        if days < 1:
            raise ValueError("Number of days must be positive.")
        assistant.birthdays_days = days
        return f"Default number of days for birthdays set to {days}."
    except ValueError as e:
        if "positive" in str(e):
            raise
        raise ValueError("Number of days must be an integer.")
