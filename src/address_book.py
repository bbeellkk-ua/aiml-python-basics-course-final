from fields import Name, Phone, Birthday, Address
from collections import UserDict
from datetime import date, timedelta
import calendar


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None

    def __str__(self):
        phones_str = ("; ".join(p.value for p in self.phones)
                      if self.phones else "no phones")
        birthday_str = str(self.birthday) if self.birthday else "no data"
        address_str = str(self.address) if self.address else "no address"
        return (
            f"Contact: {self.name.value}, phones: {phones_str}, "
            f"birthday: {birthday_str}, address: {address_str}"
        )

    def add_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone is not None:
            raise ValueError("Phone number already exists.")
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(phone)

    def find_phone(self, phone_number: str):
        return next(
            (phone for phone in self.phones if phone.value == phone_number),
            None)

    def edit_phone(self, phone_number: str, new_phone_number: str):
        phone = self.find_phone(phone_number)
        if phone is None:
            raise ValueError("Phone number not found.")
        phone.value = new_phone_number

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def add_address(self, address_str: str):
        self.address = Address(address_str)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)
        else:
            raise KeyError("Contact not found.")

    def rename(self, old_name: str, new_name: str):
        if old_name not in self.data:
            raise KeyError("Contact not found.")
        if new_name in self.data:
            raise ValueError("Contact with this name already exists.")
        record = self.data.pop(old_name)
        record.name = Name(new_name)
        self.data[new_name] = record

    def get_upcoming_birthdays(self, days: int = 7):
        def clamp_to_month_end(year: int, month: int, day: int) -> date:
            last_day = calendar.monthrange(year, month)[1]
            return date(year, month, min(day, last_day))

        def shift_to_workday(d: date) -> date:
            # 5 = Saturday, 6 = Sunday
            if d.weekday() == 5:
                return d + timedelta(days=2)
            if d.weekday() == 6:
                return d + timedelta(days=1)
            return d

        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            born_date = record.birthday.value

            birthday_this_year = clamp_to_month_end(
                today.year, born_date.month, born_date.day
            )
            if birthday_this_year >= today:
                next_birthday = birthday_this_year
            else:
                next_birthday = clamp_to_month_end(
                    today.year + 1, born_date.month, born_date.day
                )

            days_remaining = (next_birthday - today).days

            if 0 <= days_remaining < days:
                congratulation_date = shift_to_workday(next_birthday)
                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date,
                    }
                )

        upcoming_birthdays.sort(
            key=lambda x: (
                x["congratulation_date"],
                x["name"]))
        return upcoming_birthdays
