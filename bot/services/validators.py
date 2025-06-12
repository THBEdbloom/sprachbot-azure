import re
from datetime import datetime

def validate_field(field, value):
    if field in ["Vorname", "Nachname", "Ort", "Land"]:
        return value.replace(" ", "").isalpha() and len(value) >= 2

    if field == "Geburtsdatum":
        try:
            geb = datetime.strptime(value.strip(), "%d.%m.%Y")
            return geb < datetime.now() and (datetime.now().year - geb.year) < 120
        except ValueError:
            return False

    if field == "Straße":
        return len(value.strip()) >= 2

    if field == "Hausnummer":
        value = value.strip().rstrip(".")
        match = re.search(r"\d{1,4}[a-zA-Z]?", value)
        return bool(match)

    if field == "PLZ":
        return bool(re.match(r"^\d{5}$", value))

    if field == "Email":
        return "@" in value and "." in value and len(value) >= 6

    if field == "Telefonnummer":
        digits = re.sub(r"[^\d]", "", value)
        return len(digits) >= 7

    return True