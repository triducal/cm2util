# cm2util

**cm2util** is a collection of utility modules to aid in the creation of Circuit Maker 2 builds. New modules and features are still being added.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cm2util.

```bash
pip install cm2util
```

## Documentation

### Image

```python
from cm2util import Image

image = Image("path/to/image", size=50)

print(image.raw) #savecode
print(image.link) #dpaste link containing savecode
```

### Memory

```python
from cm2util import Memory
```

### Circuit

```python
from cm2util import Circuit

circuits = Circuit()

@circuits.build()
def Memory(input,save):


    and1 = circuits.AND(input,save)
    and2 = circuits.AND(save,and1)
    flip = circuits.FLIPFLOP(and1,and2)


    return flip

#Specify Bit-Length
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

saveCode = circuits.export(Byte)
print(saveCode)
```

### Compress

```python
from cm2util import Compress

dpaste_link = Compress(saveCode)
print(dpaste_link)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)