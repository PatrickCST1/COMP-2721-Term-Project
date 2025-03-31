from Wire import Wire

class Reflector:

    def __init__(self, start_connections, end_connections):
        self.wires = []

        for i in range(26):
            self.add_wire(start_connections[i], end_connections[i])

    def add_wire(self, start_connection, end_connection):
        new_wire = Wire(start_connection, end_connection)
        self.wires.append(new_wire)


    def encrypt(self, letter, direction = 1):
        converted_letter = letter

        for wire in self.wires:
            if wire.is_connected(converted_letter, direction):
                converted_letter = wire.encrypt(converted_letter, direction)
                converted_letter_as_value = ord(converted_letter) - ord('A')
                letter_as_value = converted_letter_as_value
                letter = chr(letter_as_value + ord('A'))
                return letter

