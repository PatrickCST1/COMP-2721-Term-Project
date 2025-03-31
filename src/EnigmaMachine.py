from Rotor import Rotor
from Reflector import Reflector
from Wire import Wire

class EnigmaMachine():
    def __init__(self, first_position, second_position, third_position, first_ring_setting, second_ring_setting, third_ring_setting):
        self.firstRotor = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","EKMFLGDQVZNTOWYHXUSPAIBRCJ",16, first_position, first_ring_setting)
        self.secondRotor = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", 4, second_position, second_ring_setting)
        self.thirdRotor = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", 21, third_position, third_ring_setting)
        self.reflector = Reflector("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "FVPJIAOYEDRZXWGCTKUQSBNMHL", -1)


    def encrypt(self, letter):
        self.rotate_rotors()

        encrypted_letter = letter
        encrypted_letter = self.firstRotor.encrypt(encrypted_letter, 1)
        encrypted_letter = self.secondRotor.encrypt(encrypted_letter, 1)
        encrypted_letter = self.thirdRotor.encrypt(encrypted_letter, 1)
        encrypted_letter = self.reflector.encrypt(encrypted_letter)
        encrypted_letter = self.thirdRotor.encrypt(encrypted_letter, -1)
        encrypted_letter = self.secondRotor.encrypt(encrypted_letter, -1)
        encrypted_letter = self.firstRotor.encrypt(encrypted_letter, -1)
        return encrypted_letter


    def rotate_rotors(self):
        if self.secondRotor.on_turn_over_position():
            self.thirdRotor.rotate()
            self.secondRotor.rotate()
        elif self.firstRotor.on_turn_over_position():
            self.secondRotor.rotate()
        self.firstRotor.rotate()


def main():
    machine = EnigmaMachine(13, 7, 22)
    string = "APPLE"
    for letter in string:
        print(machine.encrypt(letter), end="")

if __name__ == '__main__':
    main()
