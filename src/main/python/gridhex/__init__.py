"""Minimalistic Hex as describe in http://www.redblobgames.com/grids/hexagons/implementation.html.
"""

import math
from typing import Dict, List, Tuple

from numba import jit


class WebMercator(object):
    """Class to convert lon/lat to mercator x/y.
    """

    def __init__(self) -> None:
        """Initialize instance.
        """
        self.RAD: float = 6378137.0
        self.RAD2: float = self.RAD * 0.5
        self.LON: float = self.RAD * math.pi / 180.0
        self.D2R: float = math.pi / 180.0

    def lon_to_x(self, lon: float) -> float:
        """Geo Lon to X meters.

        :param lon: longitude value.
        :return: x in meters.
        """

        @jit(nopython=True)
        def _lon_to_x(_lon: float) -> float:
            return lon * _lon

        return _lon_to_x(self.LON)

    def lat_to_y(self, lat: float) -> float:
        """Geo Lat to Y meters.

        :param lat: latitude value.
        :return: y in meters.
        """

        @jit(nopython=True)
        def _lat_to_y(_d2r: float, _rad2: float) -> float:
            rad: float = lat * _d2r
            sin: float = math.sin(rad)
            return _rad2 * math.log((1.0 + sin) / (1.0 - sin))

        return _lat_to_y(self.D2R, self.RAD2)


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
        self.size: float = size
        self.orientation: Orientation = orientation
        self.orig_x, self.orig_y = orig
        self.xy: List[Tuple[float, float]] = []
        for i in range(7):
            angle = math.pi * ((i % 6) + orientation.ang) / 3.0
            x = size * math.cos(angle)
            y = size * math.sin(angle)
            self.xy.append((x, y))

    def to_xy(self, hex_qr: 'Hex') -> Tuple[float, float]:
        """Concert Hex to x,y.

        :param hex_qr: A Hex instance.
        :return Tuple[x,y]
        """
        m: Orientation = self.orientation
        x: float = (m.f0 * hex_qr.q + m.f1 * hex_qr.r) * self.size
        y: float = (m.f2 * hex_qr.q + m.f3 * hex_qr.r) * self.size
        return x + self.orig_x, y + self.orig_y

    def to_qr(self, x: float, y: float) -> Tuple[int, int]:
        """Convert x,y values to q,r tuple.

        :param x: The x world value.
        :param y: The y world value.
        :return: Tuple[q,r]
        """

        @jit(nopython=True)
        def _to_qr(orig_x: float, orig_y: float, size: float,
                   b0: float, b1: float, b2: float, b3: float) -> Tuple[int, int]:
            px = (x - orig_x) / size
            py = (y - orig_y) / size
            mq = b0 * px + b1 * py
            mr = b2 * px + b3 * py
            ms = -mq - mr
            q = round(mq)
            r = round(mr)
            s = round(ms)
            q_diff = abs(q - mq)
            r_diff = abs(r - mr)
            s_diff = abs(s - ms)
            if q_diff > r_diff and q_diff > s_diff:
                q = -r - s
            elif r_diff > s_diff:
                r = -q - s
            return int(q), int(r)

        m = self.orientation
        return _to_qr(self.orig_x, self.orig_y, self.size, m.b0, m.b1, m.b2, m.b3)

    def to_hex(self, x: float, y: float) -> 'Hex':
        """Convert x,y values to Hex instance.

        :param x: The x world value.
        :param y: The y world value.
        :return: Hex instance.
        """
        q, r = self.to_qr(x, y)
        return Hex(q, r)

    def to_text(self, x: float, y: float) -> str:
        """Convert x,y to hex text instance.

        :param x: the x value.
        :param y: the y value.
        :return: hex as a string.
        """
        q, r = self.to_qr(x, y)
        return f"{q}:{r}"

    def to_nume(self, x: float, y: float) -> int:
        """Convert x,y to hex nume instance.

        :param x: the x value.
        :param y: the y value.
        :return: hex as an int.
        """
        q, r = self.to_qr(x, y)
        return (q << 32) | r

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

    def __init__(self, q: int, r: int) -> None:
        """Initialize instance.

        :param q: the q value.
        :param r: the r value.
        """
        self.q = q
        self.r = r
        # self.s = -q - r

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

    def to_json(self, layout: Layout) -> Dict:
        """Return Esri JSON representation of the hex.

        :param layout: The hex layout.
        :return: Esri JSON representation.
        """
        rings = [[[x, y] for x, y in self.to_coords(layout)]]
        return {"rings": rings, "spatialReference": {"wkid": 3857}}

    def to_geojson(self, layout: Layout) -> Dict:
        """Return GeoJSON representation of the hex.

        Note: The spatial reference of the data will be in WGS84.

        :param layout: The hex layout.
        :return: GeoJSON representation.
        """

        @jit(nopython=True)
        def x_to_lon(x: float) -> float:
            return (x / 6378137.0) * (180.0 / math.pi)

        @jit(nopython=True)
        def y_to_lat(y: float) -> float:
            rad = math.pi / 2.0 - (2.0 * math.atan(math.exp(-1.0 * y / 6378137.0)))
            return rad * 180.0 / math.pi

        coordinates = [[[x_to_lon(x), y_to_lat(y)] for x, y in self.to_coords(layout)]]
        return {"type": "Polygon", "coordinates": coordinates}
