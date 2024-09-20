import numpy as np
import galois
from pyfinite import ffield
from typing import List
import utils
from utils import Converter
from keyscheduling import keyGen

class Piccolo:
    
    #S-box
    sbox = {
            "0000": [1, 1, 1, 0],
            "0001": [0, 1, 0, 0],
            "0010": [1, 0, 1, 1],
            "0011": [0, 0, 1, 0],
            "0100": [0, 0, 1, 1],
            "0101": [1, 0, 0, 0],
            "0110": [0, 0, 0, 0],
            "0111": [1, 0, 0, 1],
            "1000": [0, 0, 0, 1],
            "1001": [1, 0, 1, 0],
            "1010": [0, 1, 1, 1],
            "1011": [1, 1, 1, 1],
            "1100": [0, 1, 1, 0],
            "1101": [1, 1, 0, 0],
            "1110": [0, 1, 0, 1],
            "1111": [1, 1, 0, 1]
        }
    
    #Diffusion Matrix
    M = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]])

    def __init__(self, bit, n_rounds, master_key):
        if bit != 128 and bit != 80:
            raise ValueError
        self.bit = bit
        self.master_key = master_key
        # self.master_key_bin = Converter.convert_to_bin(self.master_key, self.bit)
        self.n_rounds= n_rounds

    def getMasterKey(self):
        return self.master_key

    def getWhiteningKeys(self):
        return keyGen.generate_whitening_keys(self.bit, self.master_key)  
    
    def getRoundKeys(self):
        return keyGen.generate_round_keys(self.bit, self.master_key, self.n_rounds)
    
    def encrypt(self, plain_text):
        wk = self.getWhiteningKeys()
        rk = self.getRoundKeys()
        # print(f"WK={wk}")
        # print(f'round keys={rk}')
        # X = Converter.convert_to_bin(plain_text, 64)
        X = utils.slice(plain_text, 64, 4)

        # X[0] = X[0] ^ wk[0]
        # X[2] = X[2] ^ wk[1]

        # rounds = 25 if self.bit==80 else 31
        rounds = self.n_rounds


        for i in range(rounds-1):
            X[1] = X[1] ^ self.ffunction(X[0]) ^ rk[2*i]
            X[3] = X[3] ^ self.ffunction(X[2]) ^ rk[(2*i)+1]
            X = self.round_permutation(X.flatten())
        
        X[1] = X[1] ^ self.ffunction(X[0]) ^ rk[(2*rounds)-2]
        X[3] = X[3] ^ self.ffunction(X[2]) ^ rk[(2*rounds)-1]

        # X[0] = X[0] ^ wk[2]
        # X[2] = X[2] ^ wk[3]

        return X.flatten(), Converter.convert_to_hex(X.flatten())
    
    
    def decrypt(self, cipher_text):
        wk = self.getWhiteningKeys()
        rk = self.getRoundKeys()
        # X = Converter.convert_to_bin(cipher_text, 64)
        X = utils.slice(cipher_text, 64, 4)
        # rounds = 25 if self.bit==80 else 31
        rounds = self.n_rounds

        rk_= np.zeros(shape=(2*rounds, 16), dtype=int)
        for i in range(rounds):
            if(i%2):
               rk_[2*i] = rk[(2*rounds)-(2*i)-1]
               rk_[(2*i)+1] = rk[(2*rounds)-(2*i)-2]
            else:        
                rk_[2*i] = rk[(2*rounds)-(2*i)-2] 
                rk_[(2*i)+1] = rk[(2*rounds)-(2*i)-1] 
    
        X[0] = X[0] ^ wk[2]
        X[2] = X[2] ^ wk[3]
        for i in range(rounds-1):
            X[1] = X[1] ^ self.ffunction(X[0]) ^ rk_[2*i]
            X[3] = X[3] ^ self.ffunction(X[2]) ^ rk_[(2*i)+1]
            X = self.round_permutation(X.flatten())
        
        X[1] = X[1] ^ self.ffunction(X[0]) ^ rk_[(2*rounds)-2]
        X[3] = X[3] ^ self.ffunction(X[2]) ^ rk_[(2*rounds)-1]

        X[0] = X[0] ^ wk[0]
        X[2] = X[2] ^ wk[1]

        return X.flatten(), Converter.convert_to_hex(X.flatten())
    
    # Pass 16 bit data and returns 16 bit data
    def ffunction(self, X):
        X = utils.slice(X, 16, 4)

        #sbox layer 1
        temp = X.copy()
        for i in range(len(temp)):
            X[i] = Piccolo.sbox[''.join(map(str, temp[i]))]
        
        temp = X.copy()
        X = np.zeros(shape=(4), dtype=int)
        for i in range(len(temp)):
            X[i] = int(''.join(map(str, temp[i])), 2)

        #M layer
        GF256 = galois.GF(2**4, irreducible_poly="x^4 + x + 1")
        M_GF = GF256(Piccolo.M)
        X_GF = GF256(X)

        temp = (M_GF @ X_GF.T).T

        # sbox layer 2
        X = np.zeros(shape=(4, 4), dtype=int)
        for i in range(len(temp)):
            X[i] = Piccolo.sbox[bin(temp[i])[2:].zfill(4)]

        return X.flatten()

    def round_permutation(self, X):
        X_8 = utils.slice(X, 64, 8)
        temp = X_8.copy()

        X_8[0] = temp[2]
        X_8[1] = temp[7]
        X_8[2] = temp[4]
        X_8[3] = temp[1]
        X_8[4] = temp[6]
        X_8[5] = temp[3]
        X_8[6] = temp[0]
        X_8[7] = temp[5]

        return utils.slice(X_8.flatten(), 64, 4)
        
    

