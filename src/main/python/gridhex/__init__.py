"""Minimalistic Hex as describe in http://www.redblobgames.com/grids/hexagons/implementation.html.
"""

import math
from typing import List, Tuple, Union, Dict

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

    def to_hex(self, x: float, y: float) -> 'Hex':
        """Convert x,y values to Hex instance."""
        m = self.orientation
        px = (x - self.orig_x) / self.size
        py = (y - self.orig_y) / self.size
        q = m.b0 * px + m.b1 * py
        r = m.b2 * px + m.b3 * py
        return Hex(q, r).round()

    def to_text(self, x: float, y: float) -> str:
        """Convert x,y to hex text instance.

        :param x: the x value.
        :param y: the y value.
        :return: hex as a string.
        """
        return self.to_hex(x, y).to_text()

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

    def _round(self) -> Tuple[int, int]:
        @jit(nopython=True)
        def __round(_q: float, _r: float, _s: float) -> Tuple[int, int]:
            q = round(_q)
            r = round(_r)
            s = round(_s)
            q_diff = abs(q - _q)
            r_diff = abs(r - _r)
            s_diff = abs(s - _s)
            if q_diff > r_diff and q_diff > s_diff:
                q = -r - s
            elif r_diff > s_diff:
                r = -q - s
            return int(q), int(r)

        return __round(float(self.q), float(self.r), float(self.s))

    def round(self) -> 'Hex':
        """Round this hex.
        """
        self.q, self.r = self._round()
        return self
