import cm2py as cm2

class Circuit:
    
    def __init__(self):
        self.save = cm2.Save()

    def build(self, *arg_bits):
        def decorator(func):
            def wrapper(*inputs):
                arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
                parentCircuit = False
                
                if not inputs:
                    parentCircuit = True
                    for arg in arg_names:
                        pos = (len(inputs)-1)*2 - int(len(arg_names)/2)
                        inputs += (self.save.addBlock(cm2.OR, (pos,0,4)),)
                    
                out = func(*inputs)
                
                if parentCircuit:
                    if not isinstance(out, tuple):
                        outputBlock = self.save.addBlock(cm2.OR, (0,0,-4))
                        self.save.addConnection(out, outputBlock)
                    else:
                        for i in range(len(out)):
                            pos = (i-1)*2 - int(len(out)/2)
                            outputBlock = self.save.addBlock(cm2.OR, (pos,0,-4))
                            self.save.addConnection(out[i], outputBlock)
            
                return out
            return wrapper
        return decorator

    def export(self, func):
        func()
        return self.save.exportSave()

    #Built-in circuits
    
    def AND(self, *inputs):
        block = self.save.addBlock(cm2.AND, (0,0,0))
        
        for input in inputs:
            self.save.addConnection(input, block)
            
        return block
    
    def NOR(self, *inputs):
        block = self.save.addBlock(cm2.NOR, (0,0,0))
        
        for input in inputs:
            self.save.addConnection(input, block)
            
        return block
    
    def NOT(self, input):
        block = self.save.addBlock(cm2.NOR, (0,0,0))
        
        self.save.addConnection(input, block)
            
        return block
    
    def NAND(self, *inputs):
        block = self.save.addBlock(cm2.NAND, (0,0,0))
        
        for input in inputs:
            self.save.addConnection(input, block)
            
        return block
    
    def OR(self, *inputs):
        block = self.save.addBlock(cm2.OR, (0,0,0))
        
        for input in inputs:
            self.save.addConnection(input, block)
            
        return block
    
    def XOR(self, *inputs):
        block = self.save.addBlock(cm2.XOR, (0,0,0))
        
        for input in inputs:
            self.save.addConnection(input, block)
            
        return block
    
    def NONE(self):
        block = self.save.addBlock(cm2.OR, (0,0,0))
        
        return block

circuits = Circuit()

@circuits.build
def ADDER(a,b,carry):
    
    xor1 = circuits.XOR(a,b)
    and1 = circuits.AND(a,b)
    
    xor2 = circuits.XOR(xor1, carry)
    and2 = circuits.AND(xor1, carry)
    
    or1 = circuits.OR(and1,and2)
    
    s = xor2
    c_out = or1
    
    return s, c_out

#Specify Bit Length
@circuits.build(a=8, b=8)
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



    
    
saveCode = circuits.export(ADDER) 
print(saveCode)