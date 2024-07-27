from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def validate_args(args: list, expected_length: int) -> None:
    if len(args) != expected_length:
        raise ValueError(f"Exactly {expected_length} argument(s) are required.")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact does not exist."
        except IndexError:
            return "Enter user name and phone."
        except Exception as e:
            return f"Error occurred: {type(e).__name__}, {e}"
    return inner

@input_error
def add_contact(args: list, contacts: AddressBook) -> str:
    validate_args(args, 2)
    name, phone = args
    record = contacts.find(name)
    if not record:
        record = Record(name)
        contacts.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args: list, contacts: AddressBook) -> str:
    validate_args(args, 3)
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if not record:
        raise KeyError("Contact does not exist.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def get_contact(args: list, contacts: AddressBook) -> str:
    validate_args(args, 1)
    name = args[0]
    record = contacts.find(name)
    if not record:
        raise KeyError("Contact does not exist.")
    return str(record)

@input_error
def get_all_contacts(contacts: AddressBook) -> str:
    if not contacts:
        return "Contacts are empty."
    contacts_list = "\n".join(str(record) for record in contacts.values())
    return f"Contacts:\n{contacts_list}"
