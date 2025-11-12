import pickle
from address_book import AddressBook
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
)


class Assistant:
    def __init__(self, filename: str = "addressbook.pkl"):
        self.filename = filename
        self.book = None

    def _load_data(self) -> AddressBook:
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()

    def _save_data(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.book, f)

    def __enter__(self):
        self.book = self._load_data()
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
            "      Add a new contact or add a new phone number to an existing contact.\n"
            "      Example: add John 1234567890\n"
            "\n"
            "  change <name> <old_phone> <new_phone>\n"
            "      Replace an existing phone number with a new one for the contact.\n"
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
            "  birthdays <days>\n"
            "      Show which contacts have a birthday coming up in the next N days.\n"
            "      Example: birthdays 7\n"
            "\n"
            "  add-address <name> <address>\n"
            "      Add or update a contact's address.\n"
            "      Example: add-birthday John US, CA, Los Angeles, Tarasa Shevchecnko, 10, 25\n"
            "\n"
            "  show-address <name>\n"
            "      Show the birthday of a contact.\n"
            "      Example: show-birthday John\n"
            "\n"
            "  help\n"
            "      Show this help message.\n"
            "\n"
            "  exit | close\n"
            "      Save data and exit the program.\n"
        )

    @staticmethod
    def invalid_input():
        print("Invalid command. Type 'help' to see available commands.")

    def run(self):
        print("Welcome to the assistant bot!")
        print("Type 'help' to see available commands.")

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
                print(add_contact(args, self.book))

            elif command == "change":
                print(change_phone(args, self.book))

            elif command == "phone":
                print(show_phone(args, self.book))

            elif command == "all":
                print(show_all(self.book))

            elif command == "add-birthday":
                print(add_birthday(args, self.book))

            elif command == "show-birthday":
                print(show_birthday(args, self.book))

            elif command == "birthdays":
                print(birthdays(args, self.book))

            elif command == "add-address":
                print(add_address(args, self.book))

            elif command == "show-address":
                print(show_address(args, self.book))

            else:
                self.invalid_input()
