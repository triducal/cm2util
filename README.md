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

@circuits.build
def Mux(D0, D1, s):

    not1 = circuits.NOT(s)
    and1 = circuits.AND(D0, not1)
    and2 = circuits.AND(D1, s)
    or1 = circuits.OR(and1, and2)

    output = or1
    return output

saveCode = circuits.export(Mux)
print(saveCode)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)