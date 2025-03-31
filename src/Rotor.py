from Wire import Wire

class Rotor:
    def __init__(self, start_connections, end_connections, turn_over_position, position=0, ring_setting=0):
        self.wires = []
        self.position = position
        self.offset = ring_setting
        self.turn_over_position = turn_over_position

        for i in range(26):
            self.add_wire(start_connections[i], end_connections[i])

    def add_wire(self, start_connection, end_connection):
        new_wire = Wire(start_connection, end_connection)
        self.wires.append(new_wire)

    def rotate(self):
        self.position = (self.position + 1) % 26

    def encrypt(self, letter, direction = 1):
        letter_as_value = ord(letter) - ord('A')
        converted_letter_as_value = (letter_as_value + self.position - self.offset) % 26
        converted_letter = chr(converted_letter_as_value + ord('A'))

        for wire in self.wires:
            if wire.is_connected(converted_letter, direction):
                converted_letter = wire.encrypt(converted_letter, direction)
                converted_letter_as_value = ord(converted_letter) - ord('A')
                letter_as_value = (converted_letter_as_value - self.position + self.offset) % 26
                letter = chr(letter_as_value + ord('A'))
                return letter

    def on_turn_over_position(self):
        return self.turn_over_position == self.position

    def get_position(self):
        return self.position

