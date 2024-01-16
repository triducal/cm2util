from PIL import Image as PIL_Image
import numpy as np
import cm2py as cm2
import requests

class Image:
    def __init__(self, image_path, size=50):
        self.raw = self.__generate(image_path, size)
        self.link = self.__createLink()

    def __generate(self, image_path, size):

        img = PIL_Image.open(image_path)
        img = img.convert('RGB')

        scale = min(1.0, size / max(*img.size))
        dim = (int(img.width * scale), int(img.height * scale))

        img = img.resize(dim)

        pixels = np.array(img)
        pixels = np.flip(pixels, axis=0)

        save = cm2.Save()

        for y in range(len(pixels)):
            for x in range(len(pixels[0])):
                rgb = pixels[y][x]
                save.addBlock(cm2.TILE, (x,y,0), properties=[rgb[0], rgb[1], rgb[2]])

        return save.exportSave()
    
    def __createLink(self):
        data = {"content": self.raw, "syntax": "text", "expiry_days": 1}
        headers = {"User-Agent": "CM2 IMAGE"}
        r = requests.post("https://dpaste.org/api/", data=data, headers=headers)
        return r.text.strip("\"") + "/raw"