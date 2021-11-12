package com.esri.hex

import scala.math.abs

/**
 * Inline hex nume calculation.
 */
object HexObj {
  /**
   * Convert x/y (web mercator) to hex nume value.
   *
   * @param xMeters      the x value in meters.
   * @param yMaters      the y value in meters.
   * @param sizeInMeters the hex size in meters.
   * @param orig         the hex layout origin in meters.
   * @param orientation  the hex orientation, flat top or pointy top.
   * @return hex nume value.
   */
  def toNume(xMeters: Double,
             yMaters: Double,
             sizeInMeters: Double,
             orig: Double = -20000000.0,
             orientation: Orientation = Orientation.TOP_FLAT
            ): Long = {
    val px = (xMeters - orig) / sizeInMeters
    val py = (yMaters - orig) / sizeInMeters
    val q = orientation.b0 * px + orientation.b1 * py
    val r = orientation.b2 * px + orientation.b3 * py
    val s = -q - r

    var qInt = q.round.toInt
    var rInt = r.round.toInt
    val sInt = s.round.toInt

    val qAbs = abs(qInt - q)
    val rAbs = abs(rInt - r)
    val sAbs = abs(sInt - s)

    if (qAbs > rAbs && qAbs > sAbs) qInt = -rInt - sInt
    else if (rAbs > sAbs) rInt = -qInt - sInt
    (qInt.toLong << 32) | (rInt.toLong & 0xFFFFFFFFL)
  }

  /**
   * Convert hex nume to X/Y meter values.
   *
   * @param nume        the hex nume.
   * @param size        the hex size.
   * @param orig        the hex origin.
   * @param orientation the hex orientation.
   * @return (x,y) in meters.
   */
  def toXY(nume: Long,
           size: Double,
           orig: Double = -20000000.0,
           orientation: Orientation = Orientation.TOP_FLAT
          ): (Double, Double) = {
    val q = nume >> 32
    val r = nume & 0xFFFFFFFFL
    val v = -(r & 0x80000000L) << 32 >> 31 | r
    val x = (orientation.f0 * q + orientation.f1 * v) * size
    val y = (orientation.f2 * q + orientation.f3 * v) * size
    (x + orig, y + orig)
  }
}
