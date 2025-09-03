import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


#TODO HOLK, das hier ist von Chat GPT Vorgeschlagen zur grafischen Visualisierung, der Flächen in der Matrix. Eventuell kann man das gut nutzen.

# ---------------------------
# Plane-Klasse
# ---------------------------
class Plane:
    def __init__(self, name, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot, matrix=None):
        self.name = name
        self.xlength = xlength
        self.ylength = ylength
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.xrot = xrot
        self.yrot = yrot
        self.zrot = zrot
        self.matrix = matrix

    @classmethod
    def __get_absolute_position_in_matrix(cls, x:int, y:int, z:int, xpos:int, ypos:int, zpos:int,
                                          xrot:int = 0, yrot:int = 0, zrot:int = 0) -> tuple[int, int, int]:
        xrad = np.radians(float(xrot))
        yrad = np.radians(float(yrot))
        zrad = np.radians(float(zrot))
        point = np.array([float(x), float(y), float(z)])

        rot_matrix_x = np.array([
            [1, 0, 0],
            [0, np.cos(xrad), -np.sin(xrad)],
            [0, np.sin(xrad), np.cos(xrad)]
        ])

        rot_matrix_y = np.array([
            [np.cos(yrad), 0, -np.sin(yrad)],
            [0, 1, 0],
            [np.sin(yrad), 0, np.cos(yrad)]
        ])

        rot_matrix_z = np.array([
            [np.cos(zrad), -np.sin(zrad), 0],
            [np.sin(zrad), np.cos(zrad), 0],
            [0, 0, 1]
        ])

        rot_point = rot_matrix_z @ (rot_matrix_y @ (rot_matrix_x @ point))
        return int(rot_point[0] + xpos), int(rot_point[1] + ypos), int(rot_point[2] + zpos)

    def get_corners(self):
        # vier Eckpunkte (x,y,z)
        corner_1 = [0, 0, 0]
        corner_2 = [self.xlength, 0, 0]
        corner_3 = [0, self.ylength, 0]
        corner_4 = [self.xlength, self.ylength, 0]
        four_corners = [corner_1, corner_2, corner_3, corner_4]

        abs_points = []
        for corner in four_corners:
            abs_points.append(
                Plane.__get_absolute_position_in_matrix(
                    corner[0], corner[1], corner[2],
                    self.xpos, self.ypos, self.zpos,
                    self.xrot, self.yrot, self.zrot
                )
            )
        return abs_points


# ---------------------------
# Utility: Check-Funktion
# ---------------------------
def check_planes_against_matrix(planes, matrix_dims):
    """
    Prüft alle Planes und gibt Punkte aus, die außerhalb der Matrix liegen.
    """
    mx, my, mz = matrix_dims
    errors_found = False

    for plane in planes:
        corners = plane.get_corners()
        for idx, (x, y, z) in enumerate(corners, start=1):
            if not (0 <= x <= mx and 0 <= y <= my and 0 <= z <= mz):
                print(f"[FEHLER] {plane.name}, Ecke {idx}: ({x}, {y}, {z}) liegt außerhalb der Matrix.")
                errors_found = True

    if not errors_found:
        print("✅ Alle Punkte liegen innerhalb der Matrix.")


# ---------------------------
# Beispiel: Matrix + Planes
# ---------------------------
matrix_dims = (150000, 80000, 5000)  # X, Y, Z
planes = [
    Plane("Test Plane 1", 10000, 2000, 20000, 2000, 2000, 0, 0, 0),
    Plane("Test Plane 2", 12000, 2500, 40000, 3000, 3000, 0, 0, 15),
    Plane("Test Plane 3", 18000, 2000, 7000, 2000, 200, 5, 2, 30),
]

# ---------------------------
# Prüfen
# ---------------------------
check_planes_against_matrix(planes, matrix_dims)

# ---------------------------
# Plotten
# ---------------------------
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

mx, my, mz = matrix_dims

# Matrix als Drahtwürfel
r = [0, mx]
s = [0, my]
t = [0, mz]
for x in r:
    for y in s:
        ax.plot([x, x], [y, y], [0, mz], color="gray", alpha=0.3)
for x in r:
    for z in t:
        ax.plot([x, x], [0, my], [z, z], color="gray", alpha=0.3)
for y in s:
    for z in t:
        ax.plot([0, mx], [y, y], [z, z], color="gray", alpha=0.3)

# Farbskala
colors = cm.get_cmap("tab10", len(planes))

# Planes
for idx, plane in enumerate(planes):
    corners = plane.get_corners()
    xs = [p[0] for p in corners]
    ys = [p[1] for p in corners]
    zs = [p[2] for p in corners]

    color = colors(idx)

    # Punkte prüfen
    in_x = (0 <= np.array(xs)) & (np.array(xs) <= mx)
    in_y = (0 <= np.array(ys)) & (np.array(ys) <= my)
    in_z = (0 <= np.array(zs)) & (np.array(zs) <= mz)
    inside = in_x & in_y & in_z

    # Punkte zeichnen
    for x, y, z, ok in zip(xs, ys, zs, inside):
        if ok:
            ax.scatter(x, y, z, s=50, color=color)
        else:
            ax.scatter(x, y, z, s=80, color="red", marker="x")

    # Fläche
    ax.plot_trisurf(xs, ys, zs, alpha=0.4, color=color)
    ax.scatter([], [], [], color=color, label=plane.name)

ax.set_xlim(0, mx)
ax.set_ylim(0, my)
ax.set_zlim(0, mz)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()
plt.show()