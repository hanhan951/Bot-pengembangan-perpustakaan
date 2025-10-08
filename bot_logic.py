import random

def gen_pass(pass_length=10):
    elements = "+-/*!&$#?=@<>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password
