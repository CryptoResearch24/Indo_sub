######## Generating the required dataset #########
from piccolo import Piccolo
import utils
import numpy as np
import os
import sys
import time
import csv
import random
import binascii
from typing import List

def generate_data(dataset_size, delta_i2, n_rounds, filename)->None:
    # fields = ['C11', 'C12','C21', 'C22', 'Cx1', 'Cx2', 'Label']  
    key_length, bits= 20, 80  #Piccolo-80
    path = "/".join(filename.split("/")[:-1])
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    with open(filename, 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile) 
        # csvwriter.writerow(fields)        # writing the fields 
        
        for i in range (0, dataset_size):
            # print(f'i={i+1}')
            row= []
            MK1 = []
            for i in range(10):
                sec = os.urandom(1)
                sec1 = int.from_bytes(sec,sys.byteorder)
                MK1.extend( list(map(int, (bin(sec1)[2:].zfill(8)))))
            piccolo= Piccolo(bits, n_rounds, MK1)

            PT1=[]
            pt1=[None]*8
            for i in range(8):
                sec = os.urandom(1)
                sec1 = int.from_bytes(sec,sys.byteorder)
                pt1[i]= sec1
                PT1.extend( list(map(int, (bin(sec1)[2:].zfill(8)))))

            CT1_binary, CT1 = piccolo.encrypt(np.asarray(PT1))
            # c11, c12= represent(CT1_binary)
            c1= convert(CT1_binary)

            ch= random.randint(0,1)
            
            if (ch==0):
                PT2=[]
                pt2=[None]*8
                for i in range(8):
                    sec = os.urandom(1)
                    sec1 = int.from_bytes(sec,sys.byteorder)
                    pt2[i]= sec1
                    PT2.extend( list(map(int, (bin(sec1)[2:].zfill(8)))))               
                label= 0
            elif ch == 1:
                pt2= [None]*8
                for i in range (8):
                    pt2[i]= pt1[i] ^ delta_i2[i]
                PT2=[]
                for sec1 in pt2:
                    PT2.extend( list(map(int, (bin(sec1)[2:].zfill(8)))))
                label =1

            CT2_binary, CT2 = piccolo.encrypt(PT2)
            # c21, c22= represent(CT2_binary)  
            c2= convert(CT2_binary)

            CX_binary= CT1_binary ^ CT2_binary
            cx1, cx2= represent(CX_binary)
            cx= convert(CX_binary)

            row.extend(c1)
            row.extend(c2)
            row.extend(cx)
            row.append(label)
            
            csvwriter.writerow(row)  
            

def represent(Y_bin):
    Y_str=[]
    Y_bin= utils.slice(Y_bin, 64, 8)
    for y in Y_bin:
        y_str=''
        y_str=''.join([str(item) for item in y])
        Y_str.append(int(y_str, 2))
    c11= ''.join([str(Y_str[item]) for item in range(0, 4)])
    c12= ''.join([str(Y_str[item]) for item in range(4, 8)])
    return c11, c12

def convert(Y_bin):
    Y_=[]
    for i in range(0, len(Y_bin), 8):
        x= ''.join(str(s) for s in Y_bin[i: i+8])
        Y_.append(int(x, 2))
    return Y_