class Hight:
    def __init__(self):
        self.SHORT_SIZE = 8    
        self.WK = [None] * 8
        self.SK = [None] * 128
        self.C = [None] * 8
        
    def final_transform(self, P):
        tmp = P[0]
        P[0] = (P[1] + self.WK[4]) & 0xFF
        P[1] = P[2]
        P[2] = P[3] ^ self.WK[5]
        P[3] = P[4]
        P[4] = (P[5] + self.WK[6]) & 0xFF
        P[5] = P[6]
        P[6] = P[7] ^ self.WK[7]
        P[7] = tmp

    def F1(self, x):
        temp1 = ((x << 3) & 0xFF) ^ ((x >> 5) & 0xFF)
        temp2 = ((x << 4) & 0xFF) ^ ((x >> 4) & 0xFF)
        temp3 = ((x << 6) & 0xFF) ^ ((x >> 2) & 0xFF)
        return temp1 ^ temp2 ^ temp3

    def F0(self, x):
        temp1 = ((x << 1) & 0xFF) ^ ((x >> 7) & 0xFF)
        temp2 = ((x << 2) & 0xFF) ^ ((x >> 6) & 0xFF)
        temp3 = ((x << 7) & 0xFF) ^ ((x >> 1) & 0xFF)
        return temp1 ^ temp2 ^ temp3

    def leftRotate(self, x, d):
        return (x << d) | (x >> (self.SHORT_SIZE - d))

    def rightRotate(self, x, d):
        return (x >> d) | (x << (self.SHORT_SIZE - d)) & 0xDDDDDF

    def round_function(self, P, sk3, sk2, sk1, sk0):
        tmp6 = P[6]
        tmp7 = P[7]
        P[7] = P[6]
        P[6] = (P[5] + (self.F1(P[4]) ^ sk2)) & 0xFF
        P[5] = P[4]
        P[4] = P[3] ^ ((self.F0(P[2]) + sk1) & 0xFF)
        P[3] = P[2]
        P[2] = (P[1] + (self.F1(P[0]) ^ sk0)) & 0xFF
        P[1] = P[0]
        P[0] = tmp7 ^ ((self.F0(tmp6) + sk3) & 0xFF)

    def initial_transform(self, P):
        P[0] = (P[0] + self.WK[0]) & 0xFF
        P[1] = P[1]
        P[2] = P[2] ^ self.WK[1]
        P[3] = P[3]
        P[4] = (P[4] + self.WK[2]) & 0xFF 
        P[5] = P[5]
        P[6] = P[6] ^ self.WK[3]
        P[7] = P[7]
        
    def encryption(self, P, n_rounds):
        self.initial_transform(P)
        for i in range(n_rounds):
            self.round_function(P, self.SK[4*i + 3], self.SK[4*i + 2], self.SK[4*i + 1], self.SK[4*i])
        self.final_transform(P)
        return P

    def const_generate(self, delta):
        s = [None] * 134
        s[0] = 0
        s[1] = 1
        s[2] = 0
        s[3] = 1
        s[4] = 1
        s[5] = 0
        s[6] = 1
        delta[0] = 0b1011010
        for i in range(1,128):
            s[i + 6] = s[i + 2] ^ s[i - 1]
            delta[i] = s[i + 6]
            for j in range(1,7):
                delta[i] <<= 1
                delta[i] ^= s[i + 6 - j]

    def subkey_generate(self, MK):
        delta = [None] * 128
        self.const_generate(delta)
        for i in range(8):
            for j in range(8):
                index = (j - i + 8) & 0x07
                self.SK[16 * i + j] = (MK[index] + delta[16*i+j]) &  0xFF
                self.SK[16 * i + j + 8] = (MK[index + 8] + delta[16*i+j+8]) & 0xFF

    def whitening_key_generate(self, MK):
        for i in range(4):
            self.WK[i] = MK[i + 12]
        for i in range(4, 8):
            self.WK[i] = MK[i - 4]
        
    def key_schedule(self, MK):
        self.whitening_key_generate(MK)
        self.subkey_generate(MK)
