import random
import string


def generate_sms_code(length=4):
    chars = string.digits
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(chars) for _ in range(length))


def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(chars) for _ in range(length))
