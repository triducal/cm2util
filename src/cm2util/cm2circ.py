import cm2py as cm2


class Circuit:
   
    def __init__(self):
        self.save = cm2.Save()
        self.bus = None


    def build(self, **arg_bits):
        def decorator(func):
            def wrapper(*inputs):
                arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
                parentCircuit = False
               
                if not inputs:
                    parentCircuit = True
                    i=0
                    for arg in arg_names:
                        if arg in arg_bits:
                            repeat = arg_bits[arg]
                            blocks = []
                            i+=1
                            for _ in range(repeat):
                                i+=1
                                pos = i
                                blocks.append(self.save.addBlock(cm2.OR, (pos,0,4)))


                            inputs += (blocks,)
                        else:
                            i+=2
                            pos = i
                            inputs += (self.save.addBlock(cm2.OR, (pos,0,4)),)
                       
                   
                out = func(*inputs)


                if out == None: return


                if parentCircuit:
                    if not isinstance(out, tuple):
                        if isinstance(out,list):
                            for y in range(len(out)):  
                                outputBlock = self.save.addBlock(cm2.OR, (y,0,-4))
                                self.save.addConnection(out[y], outputBlock)
                        else:
                            outputBlock = self.save.addBlock(cm2.OR, (0,0,-4))
                            self.save.addConnection(out, outputBlock)
                    else:
                        i=0
                        for x in range(len(out)):
                            if isinstance(out[x],list):
                                for y in range(len(out[x])):
                                    i+=1
                                    pos = i
                                    outputBlock = self.save.addBlock(cm2.OR, (pos,0,-4))
                                    self.save.addConnection(out[x][y], outputBlock)
                            else:
                                i+=2
                                pos = i
                                outputBlock = self.save.addBlock(cm2.OR, (pos,0,-4))
                                self.save.addConnection(out[x], outputBlock)
           
                return out
            return wrapper
        return decorator


    def export(self, func):
        func()
        return self.save.exportSave()
       


    #Built-in circuits


    def addConnection(self, input, block):
        self.save.addConnection(input, block)
   
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
   
    def FLIPFLOP(self, *inputs):
        block = self.save.addBlock(cm2.FLIPFLOP, (0,0,0))
       
        for input in inputs:
            self.save.addConnection(input, block)
           
        return block
