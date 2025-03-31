class Plugboard():
    def __init__(self):
        self.pairs = dict()

    def add_pair(self, first_letter, second_letter):
        if first_letter not in self.pairs.keys() and second_letter not in self.pairs.keys():
            self.pairs[first_letter] = second_letter
            self.pairs[second_letter] = first_letter

    def delete_pair(self, first_letter, second_letter):
        del self.pairs[first_letter]
        del self.pairs[second_letter]

    def encrypt(self, letter):
        if letter in self.pairs.keys():
            return self.pairs[letter]
        else:
            return letter


