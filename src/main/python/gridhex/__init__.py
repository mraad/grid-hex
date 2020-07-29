"""
    Minimalistic Hex as describe in http://www.redblobgames.com/grids/hexagons/implementation.html
"""

import math


class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Pixel({},{})".format(self.x, self.y)


class Hex:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q - r

    @staticmethod
    def from_key(key):
        lhs, rhs = key.split(":")
        q = int(lhs)
        r = int(rhs)
        return Hex(q, r)

    @staticmethod
    def from_nume(nume):
        q = int((nume >> 32) & 0xFFFFFFFF)
        r = int(nume & 0xFFFFFFFF)
        return Hex(q, r)

    def __str__(self):
        return "Hex({},{})".format(self.q, self.r)

    def to_key(self):
        return "{}:{}".format(self.q, self.r)

    def to_shape(self, layout):
        pix = layout.to_pixel(self)
        return layout.to_shape(pix.x, pix.y)

    def round(self):
        q = int(round(self.q))
        r = int(round(self.r))
        s = int(round(self.s))
        q_diff = abs(q - self.q)
        r_diff = abs(r - self.r)
        s_diff = abs(s - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        elif r_diff > s_diff:
            r = -q - s
        return Hex(q, r)


class Orientation:
    def __init__(self, f0, f1, f2, f3, b0, b1, b2, b3, ang):
        self.f0 = f0
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.ang = ang


class Layout:
    top_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0,
                             0.0, 3.0 / 2.0,
                             math.sqrt(3.0) / 3.0, -1.0 / 3.0,
                             0.0, 2.0 / 3.0,
                             0.5)
    top_flat = Orientation(3.0 / 2.0, 0.0,
                           math.sqrt(3.0) / 2.0, math.sqrt(3.0),
                           2.0 / 3.0, 0.0,
                           -1.0 / 3.0, math.sqrt(3.0) / 3.0,
                           0.0)

    def __init__(self, size, orientation, orig=Pixel(-20000000.0, -20000000.0)):
        self.size = size
        self.orientation = orientation
        self.orig = orig
        self.xy = []
        for i in range(7):
            angle = math.pi * ((i % 6) + orientation.ang) / 3.0
            x = size * math.cos(angle)
            y = size * math.sin(angle)
            self.xy.append((x, y))

    def to_pixel(self, hex):
        m = self.orientation
        x = (m.f0 * hex.q + m.f1 * hex.r) * self.size
        y = (m.f2 * hex.q + m.f3 * hex.r) * self.size
        return Pixel(x + self.orig.x, y + self.orig.y)

    def to_hex(self, x, y):
        m = self.orientation
        px = (x - self.orig.x) / self.size
        py = (y - self.orig.y) / self.size
        q = m.b0 * px + m.b1 * py
        r = m.b2 * px + m.b3 * py
        return Hex(q, r).round()

    def to_key(self, x, y):
        return self.to_hex(x, y).to_key()

    def to_shape(self, cx, cy):
        return [[cx + x, cy + y] for (x, y) in self.xy]
