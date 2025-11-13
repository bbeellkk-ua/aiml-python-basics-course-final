from fields import NoteID, NoteText

class Note:
    def __init__(self, note_id, text):
        self.id = NoteID(note_id)
        self.text = NoteText(text)

    def __str__(self):
        return f"[{self.id.value}] {self.text.value}"


class NoteBook:
    def __init__(self):
        self._notes = []
        self._note_id_counter = 1

    def add_note(self, text: str):
        note = Note(self._note_id_counter, text)
        self._notes.append(note)
        self._note_id_counter += 1
        return note

    def get_notes(self):
        return list(self._notes)

    def find_note(self, note_id):
        return next((note for note in self._notes if note.id.value == note_id), None)

    def edit_note(self, note_id: int, new_text: str):
        note = self.find_note(note_id)
        if note is None:
            raise KeyError("Note not found.")
        note.text.value = new_text

    def delete_note(self, note_id: int):
        note = self.find_note(note_id)
        if note is None:
            raise KeyError("Note not found.")
        self._notes.remove(note)
