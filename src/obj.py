class Object:
    def __init__(self):
        self.name = ""
        self._vertexes = []
        self._normals = []
        self._textures = []
        self.vertexes = []
        self.normals = []
        self.textures = []
        self.poligons = []

        self.addValues = {
            "v": self._vertexes,
            "vn": self._normals,
            "vt": self._textures,
            "f": self.poligons,
        }

    def addPoligon(self, x, y, z):
        self.poligons.append(x)
        self.poligons.append(y)
        self.poligons.append(z)

    def addElement(self, element, cords):
        self.addValues[element].append(cords)

    @staticmethod
    def loadObj(file):
        obj_file = open(file, "r")
        lines = obj_file.readlines()

        obj = Object()

        for line in lines:
            trimmed_line = line.strip()
            line_info = trimmed_line.split(" ")
            if line.startswith("o"):
                obj.name = line_info[1]
            if line_info[0] in ["v", "vn", "vt"]:
                coords = []
                for i in range(1, len(line_info)):
                    if line_info[i]:
                        coords.append(float(line_info[i]))
                obj.addElement(line_info[0], coords)
            elif line_info[0] == "f":
                x = [int(n) - 1 for n in line_info[1].split("/")]
                y = [int(n) - 1 for n in line_info[2].split("/")]
                z = [int(n) - 1 for n in line_info[3].split("/")]
                obj.addPoligon(x, y, z)

        for pair in obj.poligons:
            vert = pair[0]
            normal = pair[1]
            textura = pair[2]
            if len(obj._normals) > 0:
                for n in obj._normals[normal]:
                    obj.normals.append(n)
            if len(obj._textures) > 0:
                for c in obj._textures[textura]:
                    obj.textures.append(c)
            for v in obj._vertexes[vert]:
                obj.vertexes.append(v)
        return obj

