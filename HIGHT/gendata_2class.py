######## Generating the required dataset #########
from HIGHT import Hight
from utils import slice
import numpy as np
import os
import sys
import time
import csv
import random
from typing import List

def generate_data(dataset_size: int, n_rounds: int, filename)->None:
    listoflists = []
    for i in range(dataset_size):
      MK = [None]*16
      for i in range(16):
        sec = os.urandom(1)
        sec1 = int.from_bytes(sec, sys.byteorder)
        MK[i]= sec1
      P1 = [None] * 8
      for i in range(8):
          sec = os.urandom(1)
          sec = int.from_bytes(sec,sys.byteorder)
          P1[i] = sec
      y = random.randint(0,1)
      hight= Hight()
      hight.key_schedule(MK)
      if y == 0:
          random_plain(P1, hight, listoflists, n_rounds)
      elif y == 1:
          real_plain(P1, hight, listoflists, n_rounds)

    path = "/".join(filename.split("/")[:-1])
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file) 
        csvwriter.writerows(listoflists)
  
    
    
def real_plain(P1, hight, listoflists, n_rounds):
  l1 = []
  CX = [None] * 8
  P2 = [None] * 8
  P_real = [0x82, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
  for i in range(8):
      P2[i] = P1[i] ^ P_real[i]
  C1 = hight.encryption(P1,n_rounds)
  C2 = hight.encryption(P2,n_rounds)
  Label = 1
  for i in range(8):
    CX[i] = C1[i] ^ C2[i] 
  
  ## for sequence based models
  for i in range(8):
    l1.append(C1[i])
  for i in range(8):
    l1.append(C2[i])
  for i in range(8):
    l1.append(CX[i])
  l1.append(Label)
  listoflists.append(l1) 
 
  
def random_plain(P1, hight, listoflists, n_rounds):
  P_rand = [None] * 8
  l1 = []
  P2 = [None] * 8
  CX = [None] * 8
  
  for i in range(8):
    sec = os.urandom(1)
    sec = int.from_bytes(sec,sys.byteorder)
    P2[i] = sec
  for i in range(8):
      P_rand[i] = P1[i] ^ P2[i]
  C1 = hight.encryption(P1,n_rounds)
  C2 = hight.encryption(P2,n_rounds)
  Label = 0
  for i in range(8):
    CX[i] = C1[i] ^ C2[i] 
  for i in range(8):
    l1.append(C1[i])
  for i in range(8):
    l1.append(C2[i])
  for i in range(8):
    l1.append(CX[i])
  l1.append(Label)
  listoflists.append(l1)  
