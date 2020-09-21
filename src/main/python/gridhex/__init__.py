"""Minimalistic Hex as describe in http://www.redblobgames.com/grids/hexagons/implementation.html.
"""

from typing import List, Tuple, Union
import math
from numba import jit


class WebMercator(object):
    """Class to convert lon/lat to mercator x/y.
    """

    def __init__(self) -> None:
        """Initialize instance.
        """
        self.RAD = 6378137.0
        self.RAD2 = self.RAD * 0.5
        self.LON = self.RAD * math.pi / 180.0
        self.D2R = math.pi / 180.0

    @jit
    def lon_to_x(self, lon: float) -> float:
        """Geo Lon to X meters.

        :param lon: longitude value.
        :return: x in meters.
        """
        return lon * self.LON

    @jit
    def lat_to_y(self, lat: float) -> float:
        """Geo Lat to Y meters.

        :param lat: latitude value.
        :return: y in meters.
        """
        rad = lat * self.D2R
        sin = math.sin(rad)
        return self.RAD2 * math.log((1.0 + sin) / (1.0 - sin))


class Orientation:
    """The hex orientation; pointy or flat top.
    """

    def __init__(self,
                 f0: float, f1: float, f2: float, f3: float,
                 b0: float, b1: float, b2: float, b3: float,
                 ang: float
                 ) -> None:
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

    def __init__(self,
                 size: float,
                 orientation: Orientation = top_flat,
                 orig: Tuple[float, float] = (-20_000_000.0, -20_000_000.0)
                 ) -> None:
        """Initialize this instance.

        :param size: the hex size in meter.
        :param orientation: The hex orientation.
        :param orig: The layout origin.
        """
        self.size = size
        self.orientation = orientation
        self.orig_x, self.orig_y = orig
        self.xy = []
        for i in range(7):
            angle = math.pi * ((i % 6) + orientation.ang) / 3.0
            x = size * math.cos(angle)
            y = size * math.sin(angle)
            self.xy.append((x, y))

    @jit
    def to_xy(self, hex_qr: 'Hex') -> Tuple[float, float]:
        """Concert Hex to x,y.

        :param hex_qr: A Hex instance.
        :return Tuple[x,y]
        """
        m = self.orientation
        x = (m.f0 * hex_qr.q + m.f1 * hex_qr.r) * self.size
        y = (m.f2 * hex_qr.q + m.f3 * hex_qr.r) * self.size
        return x + self.orig_x, y + self.orig_y

    @jit
    def to_hex(self, x: float, y: float) -> 'Hex':
        """Convert x,y values to Hex instance."""
        m = self.orientation
        px = (x - self.orig_x) / self.size
        py = (y - self.orig_y) / self.size
        q = m.b0 * px + m.b1 * py
        r = m.b2 * px + m.b3 * py
        return Hex(q, r).round()

    @jit
    def to_text(self, x: float, y: float) -> str:
        """Convert x,y to hex text instance.

        :param x: the x value.
        :param y: the y value.
        :return: hex as a string.
        """
        return self.to_hex(x, y).to_text()

    @jit
    def to_nume(self, x: float, y: float) -> int:
        """Convert x,y to hex nume instance.

        :param x: the x value.
        :param y: the y value.
        :return: hex as an int.
        """
        return self.to_hex(x, y).to_nume()

    def to_coords(self, cx: float, cy: float) -> List[Tuple[float, float]]:
        """Return the hex outline coords.

        :param cx: The center x.
        :param cy: The center y.
        :return List[Tuple[x,y]]
        """
        return [(cx + x, cy + y) for (x, y) in self.xy]


class Hex:
    """Class to represent Hex cell.
    """

    def __init__(self, q: Union[int, float], r: Union[int, float]) -> None:
        """Initialize instance.

        :param q: the q value.
        :param r: the r value.
        """
        self.q = q
        self.r = r
        self.s = -q - r

    @staticmethod
    def from_text(text: str) -> 'Hex':
        """Create Hex instance from text value (q:r).
        """
        lhs, rhs = text.split(":")
        q = int(lhs)
        r = int(rhs)
        return Hex(q, r)

    @staticmethod
    def from_nume(nume: int) -> 'Hex':
        """Create Hex instance from nume value.
        """
        nume = int(nume)
        q = (nume >> 32) & 0xFFFFFFFF
        r = nume & 0xFFFFFFFF
        return Hex(q, r)

    def __str__(self) -> str:
        """Return string representation.
        """
        return "Hex({},{})".format(self.q, self.r)

    def to_text(self) -> str:
        """Convert to text value.
        """
        return "{}:{}".format(self.q, self.r)

    def to_nume(self) -> int:
        """Convert to nume value.
        """
        return (self.q << 32) | self.r

    def to_coords(self, layout: Layout) -> List[Tuple[float, float]]:
        """Return hex outline as a list of (x,y).

        :param layout: The hex layout.
        :return: list of (x,y).
        """
        x, y = layout.to_xy(self)
        return layout.to_coords(x, y)

    @jit
    def _round(self) -> Tuple[int, int]:
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
        return q, r

    def round(self) -> 'Hex':
        """Round this hex.
        """
        self.q, self.r = self._round()
        return self
