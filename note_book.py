from typing import List
from fields import NoteID, NoteText, NoteTag


class Note:
    def __init__(self, note_id, text):
        self.id = NoteID(note_id)
        self.text = NoteText(text)
        self.tags = []

    def __str__(self):
        if self.tags:
            tags_str = ", ".join(t.value for t in sorted(self.tags, key=lambda t: t.value))
            return f"[{self.id.value}] {self.text.value} (tags: {tags_str})"
        return f"[{self.id.value}] {self.text.value}"

    def add_tags(self, tags: List[NoteTag]):
        existing = {t.value for t in self.tags}
        for tag in tags:
            if tag.value not in existing:
                self.tags.append(tag)
                existing.add(tag.value)

    def remove_tags(self, tags: List[NoteTag]):
        to_remove = {t.value for t in tags}
        if not to_remove:
            return
        self.tags = [t for t in self.tags if t.value not in to_remove]

    def has_any_tag(self, tags: List[NoteTag]) -> bool:
        if not tags:
            return False
        current = {t.value for t in self.tags}
        wanted = {t.value for t in tags}
        return bool(current & wanted)


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

    def add_tags(self, note_id: int, tags: List[str]):
        note = self.find_note(note_id)
        if note is None:
            raise KeyError("Note not found.")
        tag_objs: List[NoteTag] = [NoteTag(t) for t in tags]
        note.add_tags(tag_objs)

    def remove_tags(self, note_id: int, tags: List[str]):
        note = self.find_note(note_id)
        if note is None:
            raise KeyError("Note not found.")
        tag_objs: List[NoteTag] = [NoteTag(t) for t in tags]
        note.remove_tags(tag_objs)

    def search_by_tags(self, tags: List[str]) -> List[Note]:
        tag_objs: List[NoteTag] = [NoteTag(t) for t in tags]
        if not tag_objs:
            return []
        return [n for n in self._notes if n.has_any_tag(tag_objs)]

    def sort_by_tags(self) -> List[Note]:
        def key(note: Note) -> tuple[str, int]:
            if not note.tags:
                return "~", note.id.value # no tags - to end of list, ~ is the last ASCII symbol
            first_tag = min(t.value for t in note.tags)
            return first_tag, note.id.value

        return sorted(self._notes, key=key)
