from src.cm2util import Circuit


circuits = Circuit()


#==================================
#      Arithmetic Circuits
#==================================


@circuits.build()
def ADDER(a,b,carry):
   
    xor1 = circuits.XOR(a,b)
    and1 = circuits.AND(a,b)
   
    xor2 = circuits.XOR(xor1, carry)
    and2 = circuits.AND(xor1, carry)
   
    or1 = circuits.OR(and1,and2)
   
    s = xor2
    c_out = or1
   
    return s, c_out


@circuits.build(a=8,b=8)
def ADDER_8(a, b, carry):
   
    s1,c1 = ADDER(a[0],b[0],carry)
    s2,c2 = ADDER(a[1],b[1],c1)
    s3,c3 = ADDER(a[2],b[2],c2)
    s4,c4 = ADDER(a[3],b[3],c3)
    s5,c5 = ADDER(a[4],b[4],c4)
    s6,c6 = ADDER(a[5],b[5],c5)
    s7,c7 = ADDER(a[6],b[6],c6)
    s8,c8 = ADDER(a[7],b[7],c7)


    outputByte = [s1,s2,s3,s4,s5,s6,s7,s8]
    overflow = c8


    return outputByte, overflow


@circuits.build(a=16,b=16)
def ADDER_16(a, b, carry):


    s1,c1 = ADDER_8(a[0:7],b[0:7],carry)
    s2,c2 = ADDER_8(a[8:15],b[8:15,c1])


    output = s1+s2
    overflow = c2


    return output, overflow


#==================================
#        Memory Circuits
#==================================


@circuits.build()
def Memory(input,save):


    and1 = circuits.AND(input,save)
    and2 = circuits.AND(save,and1)
    flip = circuits.FLIPFLOP(and1,and2)


    return flip


@circuits.build(input=8)
def Byte(input,save):


    m1 = Memory(input[0],save)
    m2 = Memory(input[1],save)
    m3 = Memory(input[2],save)
    m4 = Memory(input[3],save)
    m5 = Memory(input[4],save)
    m6 = Memory(input[5],save)
    m7 = Memory(input[6],save)
    m8 = Memory(input[7],save)


    out = [m1,m2,m3,m4,m5,m6,m7,m8]


    return out


@circuits.build(input=8)
def Enabler(input,e):


    a1 = circuits.AND(input[0],e)
    a2 = circuits.AND(input[1],e)
    a3 = circuits.AND(input[2],e)
    a4 = circuits.AND(input[3],e)
    a5 = circuits.AND(input[4],e)
    a6 = circuits.AND(input[5],e)
    a7 = circuits.AND(input[6],e)
    a8 = circuits.AND(input[7],e)


    out = [a1,a2,a3,a4,a5,a6,a7,a8]


    return out


@circuits.build(input=8)
def Register(input,s,e):


    mem = Byte(input,s)
    out = Enabler(mem,e)


    return out


@circuits.build()
def AND4(a,b,c,d):
    and1 = circuits.AND(a,b)
    and2 = circuits.AND(c,d)
    and3 = circuits.AND(and1,and2)


    return and3


@circuits.build()
def Decode4x16(a,b,c,d):
    a0 = circuits.NOT(a)
    b0 = circuits.NOT(b)
    c0 = circuits.NOT(c)
    d0 = circuits.NOT(d)


    d1 = AND4(a0,b0,c0,d0)
    d2 = AND4(a0,b0,c0,d)
    d3 = AND4(a0,b0,c,d0)
    d4 = AND4(a0,b0,c,d)
    d5 = AND4(a0,b,c0,d0)
    d6 = AND4(a0,b,c0,d)
    d7 = AND4(a0,b,c,d0)
    d8 = AND4(a0,b,c,d)
    d9 = AND4(a,b0,c0,d0)
    d10 = AND4(a,b0,c0,d)
    d11 = AND4(a,b0,c,d0)
    d12 = AND4(a,b0,c,d)
    d13 = AND4(a,b,c0,d0)
    d14 = AND4(a,b,c0,d)
    d15 = AND4(a,b,c,d0)
    d16 = AND4(a,b,c,d)


    out = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16]


    return out


@circuits.build(address=8,bus=8)
def RAM(address, sa, bus, s, e):
    addressReg = Byte(address, sa)
    dec_v = Decode4x16(*addressReg[0:4])
    dec_h = Decode4x16(*addressReg[4:8])


    for vi in range(16):
        for hi in range(16):
            regCheck = circuits.AND(dec_v[vi],dec_h[hi])
            saveCheck = circuits.AND(regCheck,s)
            enableCheck = circuits.AND(regCheck,e)


            register = Register(bus,saveCheck,enableCheck)
           
            for i in range(8):
                circuits.addConnection(register[i],bus[i])






saveCode = circuits.export(RAM)
print(saveCode)


