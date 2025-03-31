from Rotor import Rotor
from Reflector import Reflector
from Plugboard import Plugboard

class EnigmaMachine():
    def __init__(self, first_position= 0, second_position= 0, third_position= 0, first_ring_setting= 0, second_ring_setting= 0, third_ring_setting= 0):
        self.firstRotor = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","EKMFLGDQVZNTOWYHXUSPAIBRCJ",16, first_position, first_ring_setting)
        self.secondRotor = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", 4, second_position, second_ring_setting)
        self.thirdRotor = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", 21, third_position, third_ring_setting)
        self.reflector = Reflector("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "FVPJIAOYEDRZXWGCTKUQSBNMHL")
        self.plugboard = Plugboard()


    def encrypt(self, letter):
        self.rotate_rotors()

        encrypted_letter = letter
        encrypted_letter = self.plugboard.encrypt(encrypted_letter)
        encrypted_letter = self.firstRotor.encrypt(encrypted_letter, 1)
        encrypted_letter = self.secondRotor.encrypt(encrypted_letter, 1)
        encrypted_letter = self.thirdRotor.encrypt(encrypted_letter, 1)
        encrypted_letter = self.reflector.encrypt(encrypted_letter)
        encrypted_letter = self.thirdRotor.encrypt(encrypted_letter, -1)
        encrypted_letter = self.secondRotor.encrypt(encrypted_letter, -1)
        encrypted_letter = self.firstRotor.encrypt(encrypted_letter, -1)
        encrypted_letter = self.plugboard.encrypt(encrypted_letter)
        return encrypted_letter


    def rotate_rotors(self):
        if self.secondRotor.on_turn_over_position():
            self.thirdRotor.rotate()
            self.secondRotor.rotate()
        elif self.firstRotor.on_turn_over_position():
            self.secondRotor.rotate()
        self.firstRotor.rotate()

    def set_rotor_position(self, rotor_number, rotor_position):
        if rotor_number == 1:
            self.firstRotor.set_posiiton(rotor_position)
        elif rotor_number == 2:
            self.secondRotor.set_posiiton(rotor_position)
        elif rotor_number == 3:
            self.thirdRotor.set_posiiton(rotor_position)

    def set_rotor_ring_setting(self, rotor_number, ring_setting):
        if rotor_number == 1:
            self.firstRotor.set_offset(ring_setting)
        elif rotor_number == 2:
            self.secondRotor.set_offset(ring_setting)
        elif rotor_number == 3:
            self.thirdRotor.set_offset(ring_setting)

    def set_plugboard(self, first_letters= "ABCDEGHIJM", second_letters= "FTZKLQYNPW"):
        for first_letter, second_letters in zip(first_letters, second_letters):
            self.plugboard.add_pair(first_letter, second_letters)

    def add_plugboard_pair(self, first_letter, second_letter):
        self.plugboard.add_pair(first_letter, second_letter)

    def delete_plugboard_pair(self, first_letter, second_letter):
        self.plugboard.delete_pair(first_letter, second_letter)

def main():
    machine = EnigmaMachine(0, 0, 0, 0, 0, 0)
    machine.set_plugboard()
    string = "APPLE"
    for letter in string:
        print(machine.encrypt(letter), end="")

if __name__ == '__main__':
    main()
