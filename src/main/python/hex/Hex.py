"""
    Minimalistic Hex as describe in http://www.redblobgames.com/grids/hexagons/implementation.html 
"""


class Hex(object):
    _dirArr = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]

    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q - r

    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s

    def add(self, that):
        Hex(self.q + that.q, self.r + that.r, self.s + that.s)

    def sub(self, that):
        Hex(self.q - that.q, self.r - that.r, self.s - that.s)

    def len(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

    def distance(self, that):
        return self.sub(that).len()

    def round(self):
        q = int(round(self.q))
        r = int(round(self.r))
        s = int(round(self.s))
        q_diff = abs(q - h.q)
        r_diff = abs(r - h.r)
        s_diff = abs(s - h.s)
        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        elif r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r
        return Hex(q, r, s)

    def neighbor(self, dir):
        self.add(Hex._dirArr[dir])
