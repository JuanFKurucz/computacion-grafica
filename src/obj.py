class Object:
    def __init__(self):
        self.name = ""
        self.vertexes = []
        self.poligons = []
        self.colors = []

    def addVertex(self, x, y, z):
        self.vertexes.append(float(x))
        self.vertexes.append(float(y))
        self.vertexes.append(float(z))

    def addPoligon(self, x, y, z):
        self.poligons.append(int(x) - 1)
        self.colors.append(1)
        self.poligons.append(int(y) - 1)
        self.colors.append(1)
        self.poligons.append(int(z) - 1)
        self.colors.append(1)

    @staticmethod
    def loadObj(file):
        obj_file = open(file, "r")
        lines = obj_file.readlines()

        obj = Object()

        for line in lines:
            trimmed_line = line.strip()
            line_info = line.split(" ")
            if line.startswith("o"):
                obj.name = line_info[1]
            if line.startswith("v") or line.startswith("f"):
                try:
                    x = line_info[1]
                except IndexError:
                    x = 0
                try:
                    y = line_info[2]
                except IndexError:
                    y = 0
                try:
                    z = line_info[3]
                except IndexError:
                    z = 0
                if line.startswith("v"):
                    obj.addVertex(x, y, z)
                else:
                    obj.addPoligon(x, y, z)
        return obj

