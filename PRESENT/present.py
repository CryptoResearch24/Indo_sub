import random


class Present:
    def __init__(self, rounds):
    
        self.s_box = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
        self.inv_sbox = [self.s_box.index(x) for x in range(len(self.s_box))]
        self.p_box = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38,
            54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13,
            29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
        self.inv_p_box = [self.p_box.index(x) for x in range(64)]
        self.rounds = rounds  # 32


# sbox layer taking hexadecimal string block
    def sBoxLayer(self, state):
        sub_block = ""
        for i in range(len(state)):
            sub_block += str(hex(self.s_box[int(state[i], 16)])[2])
        return int(sub_block, 16)


    def sBoxLayerInverse(self, state):
        sub_block = ""
        for i in range(len(state)):
            sub_block += str(hex(self.inv_sbox[int(state[i], 16)])[2])
        return int(sub_block, 16)


    def sBox4Layer(self, state):
        sub_block = ""
        state = hex(int(state, 2))
        sub_block += str(hex(self.s_box[int(state, 16)])[2])
        sub_block = int(sub_block, 16)
        x = '{0:04b}'.format(sub_block)
        return x


    # pbox layer taking binary string block
    def pLayer(self, state):
        perm_block = state
        perm_list = [0 for x in range(64)]  # put 64 zeros in perm_list
        for i in range(len(state)):
            perm_list[self.p_box[i]] = state[i]
        perm_block = ''.join(perm_list)
        return int(perm_block, 2)


    def pLayerInverse(self, state):
        perm_block = state
        perm_list = [0 for x in range(64)]
        for i in range(len(state)):
            perm_list[self.inv_p_box[i]] = state[i]
        perm_block = ''.join(perm_list)
        return int(perm_block, 2)


    def xor2strings(self, string, count):
        y = '{0:05b}'.format(int(string, 2) ^ count)
        return y


    def generateRoundKeys(self, key):
        K = []  # list of 64 bit decimal keys.
        string = bin(key)[2:].zfill(80)
        K.append(int(string[:64], 2))
        for i in range(0, 31):
            string = string[61:] + string[:61]
            string = self.sBox4Layer(string[:4]) + string[4:]
            string = string[:60] + self.xor2strings(string[60:65], i + 1) + string[65:]

            # string = string[:60] +
            K.append(int(string[0:64], 2))
        return K


    def addRoundKey(self, state, K64):
        x = state ^ K64
        # x = '{0:064b}'.format(x)
        return x


    # Round Loop for Encryption
    def encrypt(self,state, K):
        for i in range(self.rounds - 1):
            # XOR with Key
            state = self.addRoundKey(state, K[i])

            # SBox
            state = hex(state)[2:].zfill(16)  # change int decimal to string hex/ zfill , fills zeros until the size is 16
            state = self.sBoxLayer(state)

            # PBox
            state = bin(state)[2:].zfill(64)
            state = self.pLayer(state)
            #print('round'+ str(i+1) + '      0x' + '{0:016x}'.format(state))
        state = self.addRoundKey(state, K[31])
        return state


    def decrypt(self, state, K):
        for i in range(self.rounds - 1):
            # XOR with Key
            state = self.addRoundKey(state, K[-i - 1])

            # Inverse PBox
            state = bin(state)[2:].zfill(64)
            state = self.pLayerInverse(state)

            # Inverse SBox
            state = hex(state)[2:].zfill(16)
            state = self.sBoxLayerInverse(state)

        state = self.addRoundKey(state, K[0])
        return state

    def hex_to_ascii_list(self, hex_value):
        # Remove the "0x" prefix (if present)
        hex_value = hex_value.lstrip("0x")

        # Split the hex string into groups of 2 characters (representing a byte)
        byte_strs = [hex_value[i:i+2] for i in range(0, len(hex_value), 2)]

        # # Convert each byte string to decimal and then to ASCII character (handle non-printable characters)
        ascii_values = []
        for byte_str in byte_strs:
            decimal_value = int(byte_str, 16)
            ascii_values.append(decimal_value)

        return ascii_values

if __name__=="__main__":

    present= Present(32)

    #test case 1
    plain = random.getrandbits(64)
    key = random.getrandbits(80)
    K = present.generateRoundKeys(key)
    cipher_text = present.encrypt(plain, K)
    print("test case 1")
    print(cipher_text)
    plain_text = present.decrypt(cipher_text, K)
    print(present.hex_to_ascii_list(hex(plain)))
    print(present.hex_to_ascii_list(hex(plain_text)))

    #test case 2
    plain = 0xFFFFFFFFFFFFFFFF
    key = 0x00000000000000000000
    K = present.generateRoundKeys(key)
    cipher_text = present.encrypt(plain, K)
    print("test case 2")
    print('0x' + '{0:016x}'.format(cipher_text))
    plain_text = present.decrypt(cipher_text, K)
    print('0x' + '{0:016x}'.format(plain_text))

    #test case 3
    plain = 0xFFFFFFFFFFFFFFFF
    key = 0xFFFFFFFFFFFFFFFFFFFF
    K = present.generateRoundKeys(key)
    cipher_text =present. encrypt(plain, K)
    print("test case 3")
    print('0x' + '{0:016x}'.format(cipher_text))
    plain_text =present. decrypt(cipher_text, K)
    print('0x' + '{0:016x}'.format(plain_text))

