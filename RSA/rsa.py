# Implimenting RSA for encryption
import random
import math


class RSA:
    def __init__(self):
        self.p, self.q = self.get_prime_numbers()
        self.N = self.p * self.q
        self.psi = (self.p - 1) * (self.q - 1)
        self.e = self.encryption_key()
        self.d = self.decryption_key()

    def random_int(self):
        return random.randint(2000, 5000)

    def is_Prime(self, num):
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def get_prime_numbers(self):
        p, q = self.random_int(), self.random_int()
        while p == q:
            q = self.random_int()

        while True:
            prime_number1 = self.is_Prime(p)
            prime_number2 = self.is_Prime(q)
            if prime_number1 and prime_number2:
                return p, q
            else:
                p = self.random_int()
                q = self.random_int()

    def encryption_key(self):
        for candidate in range(2, self.psi):
            if math.gcd(self.psi, candidate) == 1:  # defining the common divisor
                return candidate

    # get decryption key
    def decryption_key(self):
        for d in range(self.e + 1, self.N):
            if (self.e * d) % self.psi == 1:
                return d

    # encryption(5,14) decryption(11,14) if p = 2 & q = 7

    def encrypt(self, message):
        return [pow(ord(char), self.e, self.N) for char in message]

    def decrypt(self, ciphertext):
        return "".join(chr(pow(char, self.d, self.N)) for char in ciphertext)


rsa = RSA()

test = "Hello"
encrypt = rsa.encrypt(test)
decrypt = rsa.decrypt(encrypt)
print(f"Encrypted: {encrypt}, decrypted: {decrypt}")
