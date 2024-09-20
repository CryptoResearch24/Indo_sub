######## Generating the required dataset #########
from present import Present
# import utils
import numpy as np
import os
import sys
import time
import csv
import random
import binascii
from typing import List

def generate_data(dataset_size, ptd1, n_rounds, filename)->None:
    path = "/".join(filename.split("/")[:-1])
    
    if not os.path.exists(path):
      os.makedirs(path, exist_ok=True)
      
    with open(filename, 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile) 
        # csvwriter.writerow(fields)
        present= Present(n_rounds)
        for i in range (0, dataset_size):
            # print(f'i={i+1}')
                row= []
                MK= random.getrandbits(80)
                K = present.generateRoundKeys(MK)
                PT1= random.getrandbits(64)
                CT1 =  present.hex_to_ascii_list(hex(present.encrypt(PT1, K))) # coverts ti ascii value list e.g. [210, 135, 120, 160, 110, 210, 155, 169]
                c11, c12= represent(CT1)

                ch= random.randint(0,1)
                if (ch==0):
                    PT2=random.getrandbits(64)
                    label=0
                elif (ch==1):
                    PT2= PT1 ^ ptd1
                    label= 1

                CT2 =  present.hex_to_ascii_list(hex(present.encrypt(PT2, K))) # coverts ti ascii value list e.g. [210, 135, 120, 160, 110, 210, 155, 169]
                c21, c22= represent(CT2)  
                
                CT1= pad_list_to_size(CT1)
                CT2= pad_list_to_size(CT2) 
                CX= [None]*8
                for i in range (8):
                    CX[i]= CT1[i] ^ CT2[i]
                cx1, cx2= represent(CX)
                
                row.extend(CT1)
                row.extend(CT2)
                row.extend(CX)
                row.append(label)
                
                csvwriter.writerow(row)  
            
def represent(CT):
    ct1= "".join(str(c) for c in CT[:4])
    ct2= "".join(str(c) for c in CT[4:])
    return ct1, ct2

def pad_list_to_size(data_list, target_size=8, fill_value=0):
  padding_length = target_size - len(data_list)
  return [fill_value] * padding_length + data_list