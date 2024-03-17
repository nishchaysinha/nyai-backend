import random
import string


def generate_case_id():
    x = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return x