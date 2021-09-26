import re

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class Verify:
    def verify_email(email):
        if re.fullmatch(regex, email):
            return True
        else:
            return False
