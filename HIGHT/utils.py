import numpy as np

class Converter:
    hex_to_bin_dict = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
                    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
                    '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
                    'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}

    bin_to_hex_dict = {'0000': '0', '0001': '1', '0010': '2', '0011': '3',
                        '0100': '4', '0101': '5', '0110': '6', '0111': '7',
                        '1000': '8', '1001': '9', '1010': 'a', '1011': 'b',
                        '1100': 'c', '1101': 'd', '1110': 'e', '1111': 'f'}
    
    @classmethod
    def convert_to_bin(self, strvalue: str, size:int)-> np.array:
        X=np.zeros(size, dtype=int)
        i=0
        for character in strvalue.lower():
            c=Converter.hex_to_bin_dict[character]
            for item in c:
                X[i]=int(item)
                i+=1

        return X

    @classmethod
    def convert_to_hex(self, X: np.array) -> str:
        text = ""
        for set_idx in range(0, 64, 4):
            text += Converter.bin_to_hex_dict[''.join(map(str, X[set_idx:set_idx+4]))]

        return text

def slice(X: np.ndarray, bits: int, size: int) -> np.ndarray:
    increment = bits//size
    x16=np.zeros(shape=(size, increment), dtype=int)
    for i in range(0, bits, increment):
        x16[i//increment] = X[i:i+increment]

    return x16