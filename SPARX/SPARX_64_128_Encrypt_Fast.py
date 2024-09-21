#this function is the SPECKEY ARX function which performs 9 bit left rotation for the first half of the word, sum with other half of the word,14 bit left rotation for the other half and xoring other half with the first half and return the updated word 
def A(ctxt):
    a=ctxt[0]
    b=ctxt[1]
    a=((a>>7)|(a<<9))%65536
    a=(a+b)%65536
    b=((b<<2)|(b>>14))%65536
    b=b^a
    x=[a,b]
    return x


#key schedule algorithm as given in SPARX paper
def K4_128(keys,r):
    r=r+1
    keys[0:2]=A(keys[0:2])
    keys[2]=(keys[2]+keys[0])%65536
    keys[3]=(keys[3]+keys[1])%65536
    keys[7]=(keys[7]+r)%65536
    keys[0:2],keys[2:4],keys[4:6],keys[6:8]=keys[6:8],keys[0:2],keys[2:4],keys[4:6]
    return keys,r

#Linear function

def Lda(ctxt):
    a=ctxt[0]^ctxt[1]
    a=((a>>8)|(a<<(8)))%65536
    ctxts=[]
    ctxts.append(a^ctxt[0])
    ctxts.append(a^ctxt[1])
    return ctxts

#Lambda function : Performs linear function on first word and then XOR it with the second word and swap the words.

def Lamb_2(ctxt):
    a=Lda(ctxt[0:2])
    ctxt[2]=a[0]^ctxt[2]
    ctxt[3]=a[1]^ctxt[3]
    ctxt[0:2],ctxt[2:4]=ctxt[2:4],ctxt[0:2]
    return ctxt

#algorithms as given in the Paper

def sparx_64_128(pt,keys,red_rnd,n=8,w=2,rnd=3):
    key=[]
    ct=[]
    for i in keys:
        key.append(i)
    for i in pt:
        ct.append(i)
    cv=0
    flag=0
    for s in range(8):
        for i in range(w):
            for r in range(rnd):
                flag=flag+1
                ct[2*i]=ct[2*i]^key[2*r]
                ct[2*i+1]=ct[2*i+1]^key[2*r+1]
                ct[2*i:2*(i+1)]=A(ct[2*i:2*(i+1)])
                if ((s*3+r)==(red_rnd-1)):
                    # print(str(s*3+r))
                    break
            key,cv=K4_128(key,cv)
            #print(' '.join(map(str, b)))
            #print(cv)
        #b=[hex(m) for m in ct]
        if flag%3==0:
            ct=Lamb_2(ct)
        if flag==(2*red_rnd):
        	#print("OK")
            break
        #print(b)
    for i in range(w):
        ct[2*i],ct[2*i+1]=ct[2*i]^key[2*i],ct[2*i+1]^key[2*i+1]
    return ct


# Function to convert each 2-byte hex value into ASCII decimal values
def convert_to_ascii_decimal(hex_values):
    ascii_decimal_values = []
    for value in hex_values:
        # Convert decimal value to hex, format it as 4-digit hex, and split into two bytes
        hex_value = format(value, '04X')
        byte1 = int(hex_value[:2], 16)
        byte2 = int(hex_value[2:], 16)
        ascii_decimal_values.extend([byte1, byte2])
    return ascii_decimal_values


if __name__=='__main__':
    plaintxt=[0x0123, 0x4567, 0x89ab, 0xcdef]
    #plaintxt=[0x8123,0xc567, 0x89ab, 0xcdef]
    key=[0x0011, 0x2233, 0x4455, 0x6677, 0x8899, 0xaabb, 0xccdd, 0xeeff]

    print("SPARX_64_128")
    print(f"\nPlaintext: {" ".join(map(str, [hex(i) for i in plaintxt]))}")
    print(f"\nKey: {" ".join(map(str, [hex(i) for i in key]))}")
    ciphertext=sparx_64_128(plaintxt, key,red_rnd=2)
    # ciphertext=sparx_64_128(plaintxt,key,red_rnd=2)
    ascii_decimal_values = convert_to_ascii_decimal(ciphertext)
    print(ascii_decimal_values)
