import string
import random

def generate_random_string(length):
    """Generate a random string of given length."""
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))