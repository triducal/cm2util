import cm2py as cm2


class Circuit:
    
    def __init__(self):
        self.save = cm2.Save()

    def build(self, func):
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
    
    
saveCode = circuits.export(ADDER) 
print(saveCode)