class Wire:
    def __init__(self, first_connection, second_connection):
        self.first_connection = first_connection
        self.second_connection = second_connection
    def encrypt(self, letter, direction=1):
        if direction == 1:
            offset = (ord(self.second_connection) - ord(self.first_connection)) % 26
            encrypted_letter_value = (ord(letter) - ord('A') + offset) % 26
            encrypted_letter = chr(encrypted_letter_value + ord('A'))
            return encrypted_letter
        else:
            offset = (ord(self.first_connection) - ord(self.second_connection)) % 26
            encrypted_letter_value = (ord(letter) - ord('A') + offset) % 26
            encrypted_letter = chr(encrypted_letter_value + ord('A'))
            return encrypted_letter

    def is_connected(self, letter, direction=1):
        if direction == 1:
            return self.first_connection == letter
        else:
            return self.second_connection == letter
