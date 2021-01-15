class Present():
    
    def rotate_19_right(self,x):
        a=x&0b1111111111111111111#19ビット
        b=(x>>19)&0b1111111111111111111111111111111111111111111111111111111111111#61ビット

        return b^(a<<61)


    def key_sch(self,key,ROUND):
        round_key=[]
        sbox=[0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2]
        #print(len(sbox))
        reg=key
        for r in range(ROUND):
            #print( format(reg , "080b"))
            round_key.append(reg>>16)
            reg=self.rotate_19_right(reg)#19ビット右ローテート
            reg=reg&0x0fffffffffffffffffff ^ (( sbox[(reg>>76)&0xf] )<<76)
            #reg^=r<<15
            reg^=(r+1)<<15
        round_key.append(reg>>16)

        #print( format(reg , "080b"))

        return round_key

    def p_layer(self,x):
        perm=[0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,
                4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,
                8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,
                12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
        y=0
        for i in range(64):
            a=(x>>i)&1
            y^=a<<perm[i]
        return y

    def s_layer(self,x):
        sbox=[0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2]
        y=0
        for i in range(16):
            a=( x>>(i*4) )&0xf
            y^=sbox[a]<<(i*4)
        return y

    def encrypt(self,p,key,ROUND):
        x=p
        round_key=self.key_sch(key,ROUND)
        for r in range(ROUND):
            x^=round_key[r]
            x=self.s_layer(x)
            x=self.p_layer(x)
        x^=round_key[ROUND]
        y=x
        return y

    def test(self):
        #Private変数
        __key=[0x00000000000000000000,0xFFFFFFFFFFFFFFFFFFFF,0x00000000000000000000,0xFFFFFFFFFFFFFFFFFFFF]
        __plain      =[0x0000000000000000,0x0000000000000000,0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF]
        __test_vector=[0x5579C1387B228445,0xE72C46C0F5945049,0xA112FFC72F68417B,0x3333DCD3213210D2]

        for i in range(4):
            ciph=self.encrypt(__plain[i],__key[i],31)
            if(ciph!=__test_vector[i]):
                print("There are Bugs in somewhere...")
                return False #don't match with the test vecter
            print("passed test "+str(i+1))
        
        return True #match with the test vecter
"""
[To use]
from present import *
cp=Present()


[For example]
ROUND=31
plain=0x0000000000000000
key  =0xffffffffffffffffffff 
ciph =cp.encrypt(plain,key,ROUND)
print( format(ciph , "016x"))


"""