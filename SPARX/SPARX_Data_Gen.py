#import the packages
import os
import SPARX_64_128_Encrypt_Fast as sp1
import pandas as pd
import numpy as np
import sys
import time
import csv
import random
from typing import List

def generate_data(dataset_size: int, n_rounds: int, filename)->None:
    listoflists = []
    for i in range(dataset_size):
      MK = [None]*8
      for i in range(8):
        sec = os.urandom(2)
        sec1 = int.from_bytes(sec, sys.byteorder)
        MK[i]= sec1
      P1 = [None] * 4
      for i in range(4):
          sec = os.urandom(2)
          sec = int.from_bytes(sec,sys.byteorder)
          P1[i] = sec
      y = random.randint(0,1)
      if y == 0:
          random_plain(P1, MK, listoflists, n_rounds)
      elif y == 1:
          real_plain1(P1, MK, listoflists, n_rounds)

    path = "/".join(filename.split("/")[:-1])
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file) 
        csvwriter.writerows(listoflists) 
    print(f"Done round: {n_rounds}")
    
def convert_to_ascii_decimal(hex_values):
    ascii_decimal_values = []
    for value in hex_values:
        # Convert decimal value to hex, format it as 4-digit hex, and split into two bytes
        hex_value = format(value, '04X')
        byte1 = int(hex_value[:2], 16)
        byte2 = int(hex_value[2:], 16)
        ascii_decimal_values.extend([byte1, byte2])
    return ascii_decimal_values
   
def real_plain1(P1,key, listoflists, n_rounds):
    l1 = []
    cX = [None] * 4
    P2 = [None] * 4
    P_real = [0x8123,0x8123,0,0]
    for i in range(4):
        P2[i] = P1[i] ^ P_real[i]
    c1 = sp1.sparx_64_128(P1, key, n_rounds)
    c2 = sp1.sparx_64_128(P2, key, n_rounds)
    Label = 1
    for i in range(4):
        cX[i] = c1[i] ^ c2[i] 
    C1 = convert_to_ascii_decimal(c1)
    C2 = convert_to_ascii_decimal(c2)
    CX = convert_to_ascii_decimal(cX)
   
   
    l1.extend(C1)
    l1.extend(C2)
    l1.extend(CX)
    l1.append(Label)
    listoflists.append(l1) 

  
def random_plain(P1, key, listoflists, n_rounds):
    l1 = []
    P2 = [None] * 4
    cX = [None] * 4
    
    for i in range(4):
        sec = os.urandom(2)
        sec = int.from_bytes(sec,sys.byteorder)
        P2[i] = sec
    
    c1 = sp1.sparx_64_128(P1, key, n_rounds)
    c2 = sp1.sparx_64_128(P2, key, n_rounds)
    Label = 0
    for i in range(4):
        cX[i] = c1[i] ^ c2[i] 
    C1 = convert_to_ascii_decimal(c1)
    C2 = convert_to_ascii_decimal(c2)
    CX = convert_to_ascii_decimal(cX)

    l1.extend(C1)
    l1.extend(C2)
    l1.extend(CX)
    l1.append(Label)
    listoflists.append(l1)  
