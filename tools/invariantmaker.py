"""

"""

import numpy as np
from numpy.linalg import inv
import math


class InvariantMaker(object):
    def __init__(self, dimensions):
        self.round = 12
        dimX, dimY, dimZ = dimensions[0], 1, 1
        if len(dimensions) > 1:
            dimY = dimensions[1]
        if len(dimensions) > 2:
            dimZ = dimensions[2]

        simul = np.zeros([dimX * dimY * dimZ, dimX * dimY * dimZ])
        ser = -1
        for i in range(0, dimX):
            for j in range(0, dimY):
                for k in range(0, dimZ):
                    ser += 1
                    sec = -1
                    for ic in range(0, dimX):
                        for jc in range(0, dimY):
                            for kc in range(0, dimZ):
                                sec += 1
                                seCoeff = (
                                    math.pow(i, ic) * math.pow(j, jc) * math.pow(k, kc)
                                )
                                simul[ser, sec] = seCoeff

        self.alcraft = np.round(inv(simul), 14)

    def save_as_file_cpp(self, filename):
        with open(filename, "w") as fw:
            fw.write("// Automaticaly generated InvariantVandermonde matrix\n")
            fw.write("// Generated from leuci-pol interpolation library\n")
            fw.write(
                "// (c) Rachel Alcraft, 2023, Birkbeck College, London University\n\n"
            )
            shx, shy = self.alcraft.shape
            fw.write(f"double invariant_vandermonde[{shx}][{shy}] = {{\n")
            for i in range(shx):
                fw.write("    {")
                for j in range(shy):
                    v = self.alcraft[i, j]
                    if j < shy - 1:
                        fw.write(f"{v}, ")
                    else:
                        fw.write(f"{v}")
                if i < shx - 1:
                    fw.write("},\n")
                else:
                    fw.write("}\n")
            fw.write("};\n")

    def save_as_file_python(self, filename, degree):
        with open(filename, "w") as fw:
            # first the class header stuff
            fw.write("'''\n")
            fw.write("# Automaticaly generated InvariantVandermonde matrix\n")
            fw.write("# Generated from leuci-pol interpolation library\n")
            fw.write(
                "# (c) Rachel Alcraft, 2023, Birkbeck College, London University\n"
            )
            fw.write("'''\n\n")
            fw.write("import numpy as np\n")
            fw.write("class InvariantVandermonde(object):\n")
            fw.write("\tdef __init__(self):\n")
            fw.write("\t\tself.make_mat()\n")
            fw.write("\tdef get_invariant(self):\n")
            fw.write("\t\treturn self.alcraft\n")
            shx, shy = self.alcraft.shape
            fw.write("\tdef make_mat(self):\n")
            fw.write(f"\t\tself.alcraft = np.zeros(({shx},{shy}))\n")
            for i in range(shx):
                for j in range(shy):
                    v = self.alcraft[i, j]
                    # self.invariant[0, 0] = 1.0
                    fw.write(f"\t\tself.alcraft[{i},{j}]={v}\n")


if __name__ == "__main__":
    degrees = [
        # (2,),
        # (3,),
        # (4,),
        # (5,),
        # (2,2),
        # (3,3),
        # (4,4),
        (2, 2, 2),
        (3, 3, 3),
    ]
    for deg in degrees:
        im = InvariantMaker(deg)
        # filename = f"invariant_vandermonde_deg{'x'.join([str(d) for d in deg])}.py"
        # im.save_as_file_python(filename,deg)
        # print(f"Saved {filename}")
        filename = f"invariant_vandermonde_deg{'x'.join([str(d) for d in deg])}.cpp"
        im.save_as_file_cpp(filename)
        print(f"Saved {filename}")
