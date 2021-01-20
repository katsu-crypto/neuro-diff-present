class Present():
    def __init__(self,mas_key,ROUND):
        self.mas_key=mas_key#秘密鍵
        self.ROUND=ROUND#段数(フルではない)
        self.round_key=self.key_sch(self.mas_key,self.ROUND)#段鍵が保存されている配列
        self.last_round_key=self.round_key[ROUND]#最終段段鍵
        self.full_round=31


    def rotate_19_right(self,x):
        a=x&0b1111111111111111111#19ビット
        b=(x>>19)&0b1111111111111111111111111111111111111111111111111111111111111#61ビット

        return b^(a<<61)
    
    def rotate_19_left(self,x):
        #used in inverse
        a=x&0b1111111111111111111111111111111111111111111111111111111111111#61ビット
        b=(x>>61)&0b1111111111111111111#19ビット

        return b^(a<<19)


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

    def key_sch_inv(self,key,ROUND):
        sbox_inv=[0x5,0xe,0xf,0x8,0xc,0x1,0x2,0xd,0xb,0x4,0x6,0x3,0x0,0x7,0x9,0xa]
        #print(len(sbox))
        reg=key
        for r in range(ROUND):
            #print( format(reg , "080b"))
            reg=reg&0x0fffffffffffffffffff ^ (( sbox_inv[(reg>>76)&0xf] )<<76)
            reg^=(ROUND-r)<<15
            
            reg=self.rotate_19_left(reg)#19ビット左ローテート


        #print( format(reg , "080b"))

        #return round_key
        return reg

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

    def compute(self,p,round_key,ROUND):#クラス内で使う暗号化関数 処理はここで行う
        x=p
        for r in range(ROUND):
            x^=round_key[r]
            x=self.s_layer(x)
            x=self.p_layer(x)
        x^=round_key[ROUND]
        y=x
        return y

    def encrypt(self,p):#クラス外で使う暗号化関数
        y=self.compute(p,self.round_key,self.ROUND)
        return y

    def test(self):
        test_mas_key=[0x00000000000000000000,0xFFFFFFFFFFFFFFFFFFFF,0x00000000000000000000,0xFFFFFFFFFFFFFFFFFFFF]
        test_plain=[0x0000000000000000,0x0000000000000000,0xFFFFFFFFFFFFFFFF,0xFFFFFFFFFFFFFFFF]
        test_vector=[0x5579C1387B228445,0xE72C46C0F5945049,0xA112FFC72F68417B,0x3333DCD3213210D2]

        for i in range( len(test_vector) ):
            #print("plain="+format(key[i] , "016x")+", key="+format(key[i] , "020x"))
            test_round_key=self.key_sch( test_mas_key[i], self.full_round)#testメソッドでのみ使用する段鍵
            ciph=self.compute( test_plain[i], test_round_key, self.full_round)
            #print("ciph="+format(ciph , "016x")+", true cipher="+format(test_vector[i] , "016x"))
            if(ciph!=test_vector[i]):
                print("There are Bugs in present.py file...")
                return False #don't match with the test vecter
        
        return True #match with the test vecter
