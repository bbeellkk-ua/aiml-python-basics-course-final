# Python Programming. Foundations and Best Practices 2.0

## Files
- `main.py` - the bot logic itself
- `address_book.py` - the underlying classes for address book
- `assistant.py` - the class for assistant with load/save state and user input functions
- `fields.py` - classes for different fields to implement validation
- `handlers.py` - functions that implement bot actions

## Run
```bash
python3 main.py
```

<<<<<<< HEAD
## Installation via pip
```bash
pip install .
# or for development (editable install):
pip install -e .
```

## CLI Usage
After installation, run the CLI:
```bash
bot
```
=======
## Autocompletion
Tab-completion is available for commands and for the first argument when it expects a contact name.

- macOS/Linux: Uses the standard readline module. Press Tab to complete.
- macOS note: Systems using libedit are also supported; both "tab: complete" and "bind ^I rl_complete" are configured.
- Windows: The standard readline module is not available; autocompletion will be disabled. Optionally, install "pyreadline3" to enable similar behavior.

Usage:
- Start the assistant (either via "python3 main.py" or the installed CLI "address-book").
- At the prompt, type part of a command (e.g., "ad") and press Tab to complete ("add").
- For commands where the first argument is a contact name (e.g., "phone", "add-birthday"), type the beginning of a name and press Tab to complete from existing contacts.
>>>>>>> dfcd4c3 (Add autocomplete)
