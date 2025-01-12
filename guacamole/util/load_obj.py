import codecs


def loadObj(filepath):
    obj = dict()
    with codecs.open(filename=filepath, mode="r", encoding="utf8") as data:
        datalines = data.readlines()
    obj["vertices"] = []
    for dataline in datalines:
        data = dataline.split(" ")
        flag, data = data[0], data[1:]
        if flag in ["v", "vt", "vn"]:
            coords = [float(x) for x in data]
            if flag in obj:
                obj[flag].append(coords)
            else:
                obj[flag] = list([coords])
        elif flag == "f":
            faceVertice = []
            faceTexture = []
            faceNormal = []
            for item in data:
                a, b, c = [int(x) - 1 for x in item.strip().split("/")]
                faceVertice.append(obj["v"][a])
                faceTexture.append(obj["vt"][b])
                faceNormal.append(obj["vn"][c])
            faceTris = len(data) - 2
            vertexIds = [
                i + v if i > 0 else 0 for v in range(faceTris) for i in range(3)
            ]
            for vertexId in vertexIds:
                for x in faceVertice[vertexId]:
                    obj["vertices"].append(x)
                for x in faceTexture[vertexId]:
                    obj["vertices"].append(x)
                for x in faceNormal[vertexId]:
                    obj["vertices"].append(x)

    return obj["vertices"]
