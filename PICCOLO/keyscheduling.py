import utils
from utils import Converter
import numpy as np

class keyGen:
    
    @classmethod
    def generate_whitening_keys(self, bit, X_key):
        wk=np.zeros(shape=(4, 16), dtype=int)
        if(bit==80):
            k = utils.slice(X_key, 80, 5)
            wk[0]=np.concatenate((k[0][:8], k[1][8:]))
            wk[1]=np.concatenate((k[1][:8], k[0][8:]))
            wk[2]=np.concatenate((k[4][:8], k[3][8:]))
            wk[3]=np.concatenate((k[3][:8], k[4][8:]))
        elif(bit==128):
            k = utils.slice(X_key, 128, 8)
            wk[0]=np.concatenate((k[0][:8], k[1][8:]))
            wk[1]=np.concatenate((k[1][:8], k[0][8:]))
            wk[2]=np.concatenate((k[4][:8], k[7][8:]))
            wk[3]=np.concatenate((k[7][:8], k[4][8:]))
        return wk

    @classmethod
    def generate_round_keys(self, bit, X_key, rounds):
        if bit==80:
            k = utils.slice(X_key, 80, 5)
            rk = np.zeros(shape=(50, 16), dtype=int)
            # r = 25
            r = rounds
            for i in range(0, r):
                con = keyGen.con_value_80(i, bit)
                if i%5==0 or i%5==2:
                    k_2i=k[2]
                    k_2i1=k[3]
                elif i%5==1 or i%5==4:
                    k_2i=k[0]
                    k_2i1=k[1]
                elif i%5==3:
                    k_2i=k[4]
                    k_2i1=k[4]

                rk[2*i] = con[:16] ^ k_2i
                rk[(2*i)+1] = con[16:] ^ k_2i1
                
        elif bit==128:
            k = utils.slice(X_key, 128, 8)
            rk = np.zeros(shape=(62, 16), dtype=int)
            r = 31
            con= keyGen.con_value_128(bit)
            for i in range(0, 2*r):
                tmp_k = k.copy()
                if (i+2)%8==0:
                    k[0] = tmp_k[2]
                    k[2] = tmp_k[6]
                    k[3] = tmp_k[7]
                    k[4] = tmp_k[0]
                    k[5] = tmp_k[3]
                    k[6] = tmp_k[4]
                    k[7] = tmp_k[5]    
                rk[i] = k[(i+2)%8] ^ con[i]   
        return rk
    
    @classmethod
    def con_value_80(self, i, bit):
        c0 = np.array(list(bin(0)[2:].zfill(5)), dtype=int)
        ci1 = np.array(list(bin(i+1)[2:].zfill(5)), dtype=int)
        z = np.array(list('00'), dtype=int)
        xor_const = Converter.convert_to_bin("0f1e2d3c", 32) if bit==80 else Converter.convert_to_bin("6547a98b", 32)

        con = np.concatenate((ci1, c0, ci1, z, ci1, c0, ci1)) ^ xor_const
        return con
    
    @classmethod
    def con_value_128(self, bit):
        con=np.zeros(shape=(2*31, 16), dtype=int)
        c0 = np.array(list(bin(0)[2:].zfill(5)), dtype=int)
        z = np.array(list('00'), dtype=int)
        xor_const = Converter.convert_to_bin("0f1e2d3c", 32) if bit==80 else Converter.convert_to_bin("6547a98b", 32)
        
        for i in range(0, 31):
            ci1 = np.array(list(bin(i+1)[2:].zfill(5)), dtype=int)
            con_= np.concatenate((ci1, c0, ci1, z, ci1, c0, ci1)) ^ xor_const
            con[2*i] = con_[:16]
            con[(2*i)+1] = con_[16:]
        return con