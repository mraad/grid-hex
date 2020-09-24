package com.esri.hex

import scala.math.abs

/**
 * Inline hex nume calculation.
 */
object HexObj {
  /**
   * Convert x/y (def in web mercator) to hex nume value.
   *
   * @param x           the x value in meters.
   * @param y           the y value in meters.
   * @param size        the hex size.
   * @param orig        the hex layout origin.
   * @param orientation the hex orientation, flat top or pointy top.
   * @return
   */
  def toNume(x: Double,
             y: Double,
             size: Double,
             orig: Double = -20000000.0,
             orientation: Orientation = Orientation.TOP_FLAT
            ): Long = {
    val px = (x - orig) / size
    val py = (y - orig) / size
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
}
