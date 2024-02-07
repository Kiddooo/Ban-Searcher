from secrets import choice

allowedChars = [*"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"]


def generate_base64(input_length):
    generated_string = ""
    for _ in range(input_length):
        generated_string += choice(allowedChars)
    return generated_string


def verify_base64(input_string: str):
    characters = [*input_string]
    for character in characters:
        if character not in allowedChars:
            return False
    return True
