import pickle
from pathlib import Path
from address_book import AddressBook
from note_book import NoteBook
from handlers import (
    add_contact,
    show_phone,
    change_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_address,
    show_address,
    add_note,
    show_notes,
    edit_note,
    delete_note,
    tag_note,
    untag_note,
    find_notes,
    sort_notes_by_tags,
    set_birthdays_days,
)

try:
    import readline  # stdlib: tab-completion on Unix/macOS
except Exception:
    readline = None


class Assistant:
    DEFAULT_BIRTHDAYS_DAYS = 7

    def __init__(self, filename: str = "assistant.pkl"):
        # Store state under ~/.bot
        self.state_dir = Path.home() / ".bot"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        # Always store state file inside ~/.bot, using the base name to avoid
        # directory traversal
        self.filename = Path(filename).name
        self.filepath = self.state_dir / self.filename
        self.address_book = None
        self.note_book = None
        self.birthdays_days = self.DEFAULT_BIRTHDAYS_DAYS

    def _load_data(self):
        try:
            with open(self.filepath, "rb") as f:
                payload = pickle.load(f)
                self.address_book = payload.get(
                    "address_book") or AddressBook()
                self.note_book = payload.get("note_book") or NoteBook()
                self.birthdays_days = payload.get(
                    "birthdays_days", self.DEFAULT_BIRTHDAYS_DAYS
                )
        except FileNotFoundError:
            self.address_book = AddressBook()
            self.note_book = NoteBook()
            self.birthdays_days = self.DEFAULT_BIRTHDAYS_DAYS

    def _save_data(self):
        payload = {
            "address_book": self.address_book,
            "note_book": self.note_book,
            "birthdays_days": self.birthdays_days,
        }
        with open(self.filepath, "wb") as f:
            pickle.dump(payload, f)

    def __enter__(self):
        self._load_data()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._save_data()
        return False

    @staticmethod
    def _help() -> str:
        return (
            "Available commands:\n"
            "  hello\n"
            "      Greet the assistant.\n"
            "\n"
            "  add <name> <phone>\n"
            "      Add a new contact or add a new phone number to an existing"
            " contact.\n"
            "      Example: add John 1234567890\n"
            "\n"
            "  change <name> <old_phone> <new_phone>\n"
            "      Replace an existing phone number with a new one for the"
            " contact.\n"
            "      Example: change John 1234567890 555000111\n"
            "\n"
            "  phone <name>\n"
            "      Show all phone numbers for a contact.\n"
            "      Example: phone John\n"
            "\n"
            "  all\n"
            "      Show all contacts with their phone numbers and birthdays.\n"
            "\n"
            "  add-birthday <name> <DD.MM.YYYY>\n"
            "      Add or update a contact's birthday.\n"
            "      Example: add-birthday John 01.01.1990\n"
            "\n"
            "  show-birthday <name>\n"
            "      Show the birthday of a contact.\n"
            "      Example: show-birthday John\n"
            "\n"
            "  birthdays [days]\n"
            "      Show which contacts have a birthday coming up in the next"
            " N days.\n"
            "      If days is not specified, uses the configured default.\n"
            "      Example: birthdays 7\n"
            "      Example: birthdays (uses configured default)\n"
            "\n"
            "  set-birthdays-days <days>\n"
            "      Set the default number of days for the birthdays command.\n"
            "      Example: set-birthdays-days 14\n"
            "\n"
            "  add-address <name> <address>\n"
            "      Add or update a contact's address.\n"
            "      Example: add-birthday John US, CA, Los Angeles,\n"
            "      Tarasa Shevchecnko, 10, 25\n"
            "\n"
            "  show-address <name>\n"
            "      Show the birthday of a contact.\n"
            "      Example: show-birthday John\n"
            "\n"
            "  add-note <text>\n"
            "      Add a text note.\n"
            "      Example: add-note Buy milk and eggs\n"
            "\n"
            "  notes\n"
            "      List all notes.\n"
            "\n"
            "  edit-note <id> <new text>\n"
            "      Edit a note by its id.\n"
            "      Example: edit-note 3 Buy oat milk instead\n"
            "\n"
            "  delete-note <id>\n"
            "      Delete a note by its id.\n"
            "      Example: delete-note 2\n"
            "\n"
            "  tag-note <id> <tag1> [tag2] ...\n"
            "      Add one or more tags to a note.\n"
            "      Example: tag-note 1 shopping home\n"
            "\n"
            "  untag-note <id> <tag1> [tag2] ...\n"
            "      Remove one or more tags from a note.\n"
            "      Example: untag-note 1 home\n"
            "\n"
            "  find-notes <tag1> [tag2] ...\n"
            "      Find notes which contain at least one of the given tags.\n"
            "      Example: find-notes shopping home\n"
            "\n"
            "  sort-notes-by-tags\n"
            "      Show all notes sorted by tags (alphabetically).\n"
            "\n"
            "  help\n"
            "      Show this help message.\n"
            "\n"
            "  exit | close\n"
            "      Save data and exit the program.\n")

    @staticmethod
    def invalid_input():
        print("Invalid command. Type 'help' to see available commands.")

    @staticmethod
    def _match_candidates(options, prefix: str):
        if not prefix:
            return list(options)
        low = prefix.lower()
        return [o for o in options if o.lower().startswith(low)]

    def _setup_autocomplete(self):
        if readline is None:
            return

        # Known commands and those whose first argument is a contact name
        commands = [
            "hello",
            "add",
            "change",
            "phone",
            "all",
            "add-birthday",
            "show-birthday",
            "birthdays",
            "add-address",
            "show-address",
            "add-note",
            "notes",
            "edit-note",
            "delete-note",
            "tag-note",
            "untag-note",
            "find-notes",
            "sort-notes-by-tags",
            "help",
            "exit",
            "close",
        ]
        name_first_cmds = {
            "add",
            "change",
            "phone",
            "add-birthday",
            "show-birthday",
            "add-address",
            "show-address",
        }

        def completer(text, state):
            try:
                buf = readline.get_line_buffer()
            except Exception:
                buf = ""
            # Detect tokenization state
            is_new_token = buf.endswith(" ")
            tokens = buf.strip().split()

            # Determine which candidates to offer
            if not tokens or (len(tokens) == 0):
                candidates = self._match_candidates(commands, text)
            else:
                token_index = len(tokens) if is_new_token else max(
                    len(tokens) - 1, 0)

                if token_index == 0:
                    # Completing the command name
                    # Use the full first token as prefix to avoid delimiter
                    # issues (e.g., hyphen)
                    cmd_prefix = tokens[0] if not is_new_token else ""
                    candidates = self._match_candidates(commands, cmd_prefix)
                elif (
                    tokens and tokens[0].lower(
                    ) in name_first_cmds and token_index == 1
                ):
                    # Completing the first argument (contact name)
                    names = (list(self.address_book.data.keys())
                             if self.address_book else [])
                    candidates = self._match_candidates(names, text)
                else:
                    candidates = []

            try:
                return sorted(candidates)[state]
            except IndexError:
                return None

        try:
            # Bind both GNU readline and libedit (macOS) styles
            try:
                readline.set_completer_delims(" \t")
            except Exception:
                pass
            readline.set_completer(completer)
            try:
                readline.parse_and_bind("tab: complete")
            except Exception:
                pass
            try:
                readline.parse_and_bind("bind ^I rl_complete")
            except Exception:
                pass
        except Exception:
            # Fail silently if readline is unavailable or misconfigured
            pass

    def run(self):
        print("Welcome to the assistant bot!")
        print("Type 'help' to see available commands.")
        self._setup_autocomplete()

        while True:
            try:
                user_input = input("Enter a command: ")
                command, *args = user_input.split()
                command = command.strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nGood bye!")
                break
            except ValueError:
                self.invalid_input()
                continue

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "help":
                print(self._help())

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, self.address_book))

            elif command == "change":
                print(change_phone(args, self.address_book))

            elif command == "phone":
                print(show_phone(args, self.address_book))

            elif command == "all":
                print(show_all(self.address_book))

            elif command == "add-birthday":
                print(add_birthday(args, self.address_book))

            elif command == "show-birthday":
                print(show_birthday(args, self.address_book))

            elif command == "birthdays":
                print(birthdays(args, self.address_book, self.birthdays_days))

            elif command == "set-birthdays-days":
                print(set_birthdays_days(args, self))

            elif command == "add-address":
                print(add_address(args, self.address_book))

            elif command == "show-address":
                print(show_address(args, self.address_book))

            elif command == "add-note":
                print(add_note(args, self.note_book))

            elif command == "notes":
                print(show_notes(self.note_book))

            elif command == "edit-note":
                print(edit_note(args, self.note_book))

            elif command == "delete-note":
                print(delete_note(args, self.note_book))

            elif command == "tag-note":
                print(tag_note(args, self.note_book))

            elif command == "untag-note":
                print(untag_note(args, self.note_book))

            elif command == "find-notes":
                print(find_notes(args, self.note_book))

            elif command == "sort-notes-by-tags":
                print(sort_notes_by_tags(args, self.note_book))

            else:
                self.invalid_input()
