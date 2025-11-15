# Python Programming. Foundations and Best Practices 2.0

Address Book CLI assistant bot that manages contacts (phones, birthdays, addresses) and simple notes with tags. Provides a local persistence file, a packaged CLI, and command autocompletion on supported systems.

## Project layout (paths)

```
.
├─ README.md
├─ pyproject.toml                     # Packaging metadata; exposes CLI entrypoint "bot"
├─ src/
│  ├─ main.py                         # Entry point (def main()) used by CLI and local runs
│  ├─ assistant.py                    # Assistant lifecycle, REPL loop, state persistence, autocomplete
│  ├─ address_book.py                 # Record and AddressBook classes (contacts, birthdays, addresses)
│  ├─ fields.py                       # Field types and validation (Phone, Birthday, Note IDs, Tags, etc.)
│  ├─ handlers.py                     # All command handlers wired by assistant (add, change, notes, etc.)
│  └─ note_book.py                    # Notes, tags, search, sort
```

## Key files and modules

- src/main.py — program entry point (main()) used by the CLI and for local runs
- src/assistant.py — Assistant class (context manager), REPL loop, state save/load, autocompletion
- src/address_book.py — Record and AddressBook with phones, birthday calculations, addresses
- src/fields.py — Field types and validation rules (Phone, Birthday, NoteID, NoteText, NoteTag, etc.)
- src/handlers.py — User command handlers (add/change/phone/all/birthdays/address/note operations)
- src/note_book.py — Note storage with tags, search by tags, sorting
- pyproject.toml — Project metadata and CLI definition (`bot = "main:main"`)

## How to run (from source, without installing)

From the repository root, either:
```bash
python3 src/main.py
```

## Installation via pip

```bash
pip install .
# or for development (editable install)
pip install -e .
```

## CLI usage (after installation)

The package installs the CLI entrypoint named `bot`:

```bash
bot
```

This starts the interactive assistant.

## Autocompletion

Tab-completion is available for commands and for the first argument when it expects a contact name.

- macOS/Linux: Uses the standard readline module. Press Tab to complete.
- macOS note: Systems using libedit are also supported; both "tab: complete" and "bind ^I rl_complete" are configured.
- Windows: The standard readline module is not available; autocompletion will be disabled. Optionally, install "pyreadline3" to enable similar behavior.

Usage:
- Start the assistant (either via "python3 src/main.py" or the installed CLI "bot").
- At the prompt, type part of a command (e.g., "ad") and press Tab to complete ("add").
- For commands where the first argument is a contact name (e.g., "phone", "add-birthday"), type the beginning of a name and press Tab to complete from existing contacts.

## Persistence (where your data is stored)

By default the assistant stores its state in:
- ~/.bot/assistant.pkl

This includes contacts, notes, and the configured default number of days for the `birthdays` command.
