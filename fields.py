from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits (0-9).")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        self._value = value



class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        try:
            parsed_date = datetime.strptime(new_value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self._value = parsed_date

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
