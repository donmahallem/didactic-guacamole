import codecs


def loadObj(filepath):
    obj = dict()
    with codecs.open(filename=filepath, mode="r", encoding="utf8") as data:
        datalines = data.readlines()
    for dataline in datalines:
        data = dataline.split(" ")
        flag, data = data[0], data[1:]
        if flag in ["v", "vt", "vn"]:
            coords = [float(x) for x in data]
            if flag in obj:
                obj[flag].append(coords)
            else:
                obj[flag] = list(coords)
        elif flag == "f":
            faceVertice = []
            faceTexture = []
            faceNormal = []
            for item in data:
                a, b, c = [int(x) - 1 for x in item.strip().split("/")]
                faceVertice.append(a)
                faceTexture.append(b)
                faceNormal.append(c)
