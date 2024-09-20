import math
import struct
import math, os,sys
import random
import numpy as np
import csv

C = [None] * 16
delta = [None] * 8

T = [None] * 4
RK = [None] * 6

#Plain Text Generation
def Plaintext_Generation(a):
  P = [None] * 4
  for i in range(16):
      a[i] = hex(a[i])
      #print(a[i])
      a[i] = a[i].replace('0x','')
      if len(a[i]) < 2:
          a[i] = '0' + a[i]
  for i in range(4):
      P[i] = '0x' + a[4*i + 3] + a[4*i + 2] + a[4*i + 1] + a[4*i]
      #print(P[i])
      P[i] = int(P[i],16)
      #print(P[i])
  return P

#Key Generation
def Key_Generation(key):
  K = [None] * 4
  for i in range(16):
      key[i] = hex(key[i])
      #print(a[i])
      key[i] = key[i].replace('0x','')
      if len(key[i]) < 2:
          key[i] = '0' + key[i]
  for i in range(4):
      K[i] = '0x' + key[4*i + 3] + key[4*i + 2] + key[4*i + 1] + key[4*i]
      #print(P[i])
      K[i] = int(K[i],16)
      #print(K[i])
  return(K)


delta[0] = 0xc3efe9db
delta[1] = 0x44626b02
delta[2] = 0x79e27c8a
delta[3] = 0x78df30ec
delta[4] = 0x715ea49e
delta[5] = 0xc785da0a
delta[6] = 0xe04ef22a
delta[7] = 0xe5c40957

#Left Circular Rotation
def lrotate(input,d):
    # slice string in two parts for left and right
    Lfirst = input[0 : d]
    Lsecond = input[d :]
    Rfirst = input[0 : len(input)-d]
    Rsecond = input[len(input)-d : ]
    # now concatenate two parts together
    return(Lsecond + Lfirst)
    #print ("Right Rotation : ", (Rsecond + Rfirst))

#Right Circular Rotation
def rrotate(input,d):
    # slice string in two parts for left and right
    Lfirst = input[0 : d]
    Lsecond = input[d :]
    Rfirst = input[0 : len(input)-d]
    Rsecond = input[len(input)-d : ]
    # now concatenate two parts together
    #print ("Left Rotation : ", (Lsecond + Lfirst) )
    return(Rsecond + Rfirst)

#Key Schedule Function Generation of Round Keys
def key_schedule(K,T,delta,i):
  tmp = delta[i % 4]
  tmp = bin(tmp)
  tmp = str(tmp)
  tmp = tmp.replace("0b",'')
  if len(tmp) < 32:
    dif = 32 - len(tmp)
    times = '0' 
    for i in range(dif - 1):
      times = times + '0'
    tmp = times + tmp
  #print(len(tmp))
  t1 = lrotate(tmp,i)
  t1 = int(t1,2)
  t2 = lrotate(tmp,i+1)
  t2 = int(t2,2)
  t3 = lrotate(tmp,i+2)
  t3 = int(t3,2)
  t4 = lrotate(tmp,i+3)
  t4 = int(t4,2)
  tm1 = (T[0] + t1) % 2**32
  tm2 = (T[1] + t2) % 2**32
  tm3 = (T[2] + t3) % 2**32
  tm4 = (T[3] + t4) % 2**32
  tm1 = bin(tm1)
  tm2 = bin(tm2)
  tm3 = bin(tm3)
  tm4 = bin(tm4)
  tm1 = str(tm1)
  tm2 = str(tm2)
  tm3 = str(tm3)
  tm4 = str(tm4)
  tm1 = tm1.replace("0b",'')
  tm2 = tm2.replace("0b",'')
  tm3 = tm3.replace("0b",'')
  tm4 = tm4.replace("0b",'')
  #print(tm1,tm2,tm3,tm4)
  #tm1
  if len(tm1) < 32:
    dif1 = 32 - len(tm1)
    times1 = '0' 
    for i in range(dif1 - 1):
      times1 = times1 + '0'
    tm1 = times1 + tm1

  #tm2
  if len(tm2) < 32:
    dif2 = 32 - len(tm2)
    times2 = '0' 
    for i in range(dif2 - 1):
      times2 = times2 + '0'
    tm2 = times2 + tm2

  #tm3
  if len(tm3) < 32:
    dif3 = 32 - len(tm3)
    times3 = '0' 
    for i in range(dif3 - 1):
      times3 = times3 + '0'
    tm3 = times3 + tm3

  #tm4
  if len(tm4) < 32:
    dif4 = 32 - len(tm4)
    times4 = '0' 
    for i in range(dif4 - 1):
      times4 = times4 + '0'
    tm4 = times4 + tm4
  #print(tm1,tm2,tm3,tm4)
  f1 = lrotate(tm1,1)
  f2 = lrotate(tm2,3)
  f3 = lrotate(tm3,6)
  f4 = lrotate(tm4,11)
  #print(f1,f2,f3,f4)
  T[0] = int(f1,2)
  T[1] = int(f2,2)
  T[2] = int(f3,2)
  T[3] = int(f4,2)
  rk = f1 + f2 + f3 + f2 + f4 + f2
  #print(len(rk))
  #print(rk)
  #print(T[0],T[1],T[2],T[3])
  return rk


#encryption function
def encrypt(P,K,rk,RK):
  r1 = rk[0:32]
  r2 = rk[32:64]
  r3 = rk[64:96]
  r4 = rk[96:128]
  r5 = rk[128:160]
  r6 = rk[160:192]
  #print(r1,r2,r3,r4,r5,r6)
  r1 = int(r1,2)
  r2 = int(r2,2)
  r3 = int(r3,2)
  r4 = int(r4,2)
  r5 = int(r5,2)
  r6 = int(r6,2)
  #print(r1,r2,r3,r4,r5,r6)
  RK[0] = r1
  RK[1] = r2
  RK[2] = r3
  RK[3] = r4
  RK[4] = r5
  RK[5] = r6
  tmp = P[0]
  u1 = P[0] ^ RK[0]
  u2 = P[1] ^ RK[2]
  u3 = P[2] ^ RK[4]
  v1 = P[1] ^ RK[1]
  v2 = P[2] ^ RK[3]
  v3 = P[3] ^ RK[5]
  uv1 = (u1 + v1) % 2**32
  uv2 = (u2 + v2) % 2**32
  uv3 = (u3 + v3) % 2**32
  uv1 = bin(uv1)
  uv1 = str(uv1)
  uv1 = uv1.replace("0b",'')

  uv2 = bin(uv2)
  uv2 = str(uv2)
  uv2 = uv2.replace("0b",'')

  uv3 = bin(uv3)
  uv3 = str(uv3)
  uv3 = uv3.replace("0b",'')
  #print(uv1,uv2,uv3)

  if len(uv1) < 32:
    dif1 = 32 - len(uv1)
    times1 = '0' 
    for i in range(dif1 - 1):
      times1 = times1 + '0'
    uv1 = times1 + uv1
  
  if len(uv2) < 32:
    dif2 = 32 - len(uv2)
    times2 = '0' 
    for i in range(dif2 - 1):
      times2 = times2 + '0'
    uv2 = times2 + uv2

  if len(uv3) < 32:
    dif3 = 32 - len(uv3)
    times3 = '0' 
    for i in range(dif3 - 1):
      times3 = times3 + '0'
    uv3 = times3 + uv3
  #print(uv1,uv2,uv3)
  f1 = lrotate(uv1,9)
  f2 = rrotate(uv2,5)
  f3 = rrotate(uv3,3)
  #print(f1,f2,f3)
  f1 = int(f1,2)
  f2 = int(f2,2)
  f3 = int(f3,2)
  #print(f1,f2,f3)
  P[0] = f1
  P[1] = f2
  P[2] = f3
  P[3] = tmp

############################################
#Together 
def encryption(P,K,delta,RK):
  for i in range(4):
    T[i] = K[i]
  for i in range(n_rounds):
    rk = key_schedule(K,T,delta,i)
    encrypt(P,K,rk,RK)
    #print("Plain text at round ",i,"is",P)
  return P
##############################################


def real_plain(P1):
  l1 = []
  P_real_main = [None]*4
  del_L = [None] * 2
  del_R = [None] * 2
  P2 = [None] * 4
  K = [None] * 4
  CX= [None] * 4
  
  P_real_main = [0x80000080, 0x80000080, 0x80000010, 0x80000014]

  key = [None] * 16
  for i in range(16):
    sec = os.urandom(1)
    sec = int.from_bytes(sec,sys.byteorder)
    key[i] = sec
  K = Key_Generation(key)
  for i in range(4):
      P2[i] = P1[i] ^ P_real_main[i]
  # print(f'P_2={P_2}')
  # print(f'P2={P2}')
  C1 = encryption(P1,K,delta,RK)
  C2 = encryption(P2,K,delta,RK)
  for i in range (len (C1)):
    CX[i]= C1[i] ^ C2[i]

  C1= struct.pack('<LLLL',C1[0], C1[1], C1[2], C1[3])
  C1= list(C1)

  C2= struct.pack('<LLLL',C2[0], C2[1], C2[2], C2[3])
  C2= list(C2)

  CX= struct.pack('<LLLL',CX[0], CX[1], CX[2], CX[3])
  CX= list(CX)

  # print(f"C1={C1}")
  # print(f'C2={C2}')
  Label = 1
  #print("Label: ",Label,"C1: ",C1,"C2",C2)
  
  for i in range (len (C1)):
     l1.append(C1[i])

  for i in range (len (C2)):
     l1.append(C2[i])

  for i in range (len (CX)):
     l1.append(CX[i])
  
  l1.append(Label)
  listoflists.append(l1)
  

###### RANDOM PLAIN DIFF #####  
def random_plain(P1):
  #P_rand = [None] * 4
  l1 = []
  P2 = [None] * 4
  del_L = [None] * 2
  del_R = [None] * 2
  K = [None] * 4
  CX= [None] * 4
  key = [None] * 16
  P_2 = [None] * 16
  for i in range(16):
    sec = os.urandom(1)
    sec = int.from_bytes(sec,sys.byteorder)
    P_2[i] = sec
  P2 = Plaintext_Generation(P_2)
  # print(f'P_2={P_2}')
  # print(f'P2={P2}')
  for i in range(16):
    sec = os.urandom(1)
    sec = int.from_bytes(sec,sys.byteorder)
    key[i] = sec
  K = Key_Generation(key)
  
  C1 = encryption(P1,K,delta,RK)
  C2 = encryption(P2,K,delta,RK)
  for i in range (len (C1)):
    CX[i]= C1[i] ^ C2[i]

  C1= struct.pack('<LLLL',C1[0], C1[1], C1[2], C1[3])
  C1= list(C1)

  C2= struct.pack('<LLLL',C2[0], C2[1], C2[2], C2[3])
  C2= list(C2)

  CX= struct.pack('<LLLL',CX[0], CX[1], CX[2], CX[3])
  CX= list(CX)
  Label = 0
  # print(f"C1={C1}")
  # print(f'C2={C2}')
  #print("Label: ",Label,"C1: ",C1,"C2",C2)
  for i in range (len (C1)):
     l1.append(C1[i])

  for i in range (len (C2)):
     l1.append(C2[i])

  for i in range (len (CX)):
     l1.append(CX[i])
  
  l1.append(Label)
  listoflists.append(l1)


datasetsize = 100000
for n_rounds in range(5, 6): #specify the rounds
    listoflists = []
    for _ in range(datasetsize):
        P_1 = [None] * 16
        for i in range(16):
            sec = os.urandom(1)
            sec = int.from_bytes(sec,sys.byteorder)
            P_1[i] = sec
        # print(f'P_1={P_1}')
        P1 = Plaintext_Generation(P_1)
        # print(f'P={P1}')
        y = random.randint(0,1)
        if y == 0:
            random_plain(P1)
        elif y == 1:
            real_plain(P1)
    
    # print(listoflists)
    filename = f'./data/LEA_Round_{n_rounds}.csv'
    path = "/".join(filename.split("/")[:-1])
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file) 
        csvwriter.writerows(listoflists) 