class Enigma:

    def __init__(self, reflector, rotor1, rotor2, rotor3, plugboard, keyboard):
        self.reflector = reflector
        self.rotor1 = rotor1
        self.rotor2 = rotor2
        self.rotor3 = rotor3
        self.plugboard = plugboard
        self.keyboard = keyboard

    def setRings(self, rings):
        self.rotor1.setRing(rings[0])
        self.rotor2.setRing(rings[1])
        self.rotor3.setRing(rings[2])
    def setRotor(self, key):
        self.rotor1.rotate_to(key[0])
        self.rotor2.rotate_to(key[1])
        self.rotor3.rotate_to(key[2])

    def encipher(self, letter, path):
        if letter == ' ':
            return letter

        if self.rotor2.left[0] == self.rotor2.notch and self.rotor3.left[0] == self.rotor3.notch:
            self.rotor1.rotate()
            self.rotor2.rotate()
            self.rotor3.rotate()
        elif self.rotor2.left[0] == self.rotor2.notch:
            self.rotor1.rotate()
            self.rotor2.rotate()
            self.rotor3.rotate()
        elif self.rotor1.left[0] == self.rotor3.notch:
            self.rotor2.rotate()
            self.rotor1.rotate()
        else:
            self.rotor1.rotate()

        path = " "

        signal = self.keyboard.forward(letter)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.plugboard.forward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.rotor3.forward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.rotor2.forward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.rotor1.forward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.reflector.reflect(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.rotor1.backward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.rotor2.backward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.rotor3.backward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + "->"
        signal = self.plugboard.backward(signal)
        path = path + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[signal] + " "
        letter = self.keyboard.backward(signal)

        return letter, path