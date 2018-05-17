from django.utils.crypto import get_random_string
　
　
def gen_secret_key(length):
    if length < 50:
        length = 50  # minimum length is 50
　
    # Generating secret key same way Django uses in 'startproject'
    # See: https://github.com/django/django/blob/9893fa12b735f3f47b35d4063d86dddf3145cb25/django/core/management/commands/startproject.py
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(length, chars)
