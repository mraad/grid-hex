package com.esri.hex

import scala.collection.mutable.ArrayBuffer
import scala.math.abs

/**
  * Class to convert hex coordinate to and from world coordinates.
  *
  * @param origX       the world x origin.
  * @param origY       the world y origin.
  * @param sizeX       the hex x size.
  * @param sizeY       the hex y size.
  * @param orientation the hex orientation (flat top or pointy top).
  */
case class Layout(origX: Double, origY: Double, sizeX: Double, sizeY: Double, orientation: Orientation = Orientation.TOP_FLAT) {

  @inline
  private def qr2xy(q: Int, r: Int): (Double, Double) = {
    val x = (orientation.f0 * q + orientation.f1 * r) * sizeX
    val y = (orientation.f2 * q + orientation.f3 * r) * sizeY
    (x + origX, y + origY)
  }

  /**
    * Convert a hex coordinate to world coordinates.
    *
    * @param h the hex to convert
    * @return (x,y)
    */
  def hexToXY(h: Hex): (Double, Double) = {
    //    val x = (orientation.f0 * h.q + orientation.f1 * h.r) * sizeX
    //    val y = (orientation.f2 * h.q + orientation.f3 * h.r) * sizeY
    //    (x + origX, y + origY)
    qr2xy(h.q, h.r)
  }

  /**
    * Convert world coordinate to a Hex instance.
    *
    * @param x the world x coordinate.
    * @param y the world y coordinate.
    * @return a FractionalHex instance.
    */
  def xyToHex(x: Double, y: Double): FractionalHex = {
    val px = (x - origX) / sizeX
    val py = (y - origY) / sizeY
    val q = orientation.b0 * px + orientation.b1 * py
    val r = orientation.b2 * px + orientation.b3 * py
    FractionalHex(q, r, -q - r)
  }

  @inline
  private def xy2qr(x: Double, y: Double): (Int, Int) = {
    val px = (x - origX) / sizeX
    val py = (y - origY) / sizeY
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
    (qInt, rInt)
  }

  /**
    * Convert world coordinate to a QR hex text (q:r).
    *
    * @param x the world x coordinate.
    * @param y the world y coordinate.
    * @return a key as a String instance (q:r).
    */
  def xyToText(x: Double, y: Double): String = {
    val (qInt, rInt) = xy2qr(x, y)
    s"$qInt:$rInt"
  }

  /**
    * Convert QR text hex value to world coordinates.
    *
    * @param key the hex key.
    * @return Tuple[x,y]
    */
  def textToXY(key: String): (Double, Double) = {
    key.split(':') match {
      case Array(q, r) => {
        qr2xy(q.toInt, r.toInt)
      }
      case _ => (0.0, 0.0)
    }
  }

  /**
    * Convert world coordinate to a QR hex nume.
    *
    * @param x the world x coordinate.
    * @param y the world y coordinate.
    * @return a key as a Long instance.
    */
  def xyToNume(x: Double, y: Double): Long = {
    val (qInt, rInt) = xy2qr(x, y)
    (qInt.toLong << 32) | (rInt.toLong & 0xFFFFFFFFL)
  }

  /**
    * Convert QR hex nume to world coordinates.
    *
    * @param nume the qr nume value.
    * @return (x,y)
    */
  def numeToXY(nume: Long): (Double, Double) = {
    val q = nume >> 32
    val r = nume & 0xFFFFFFFFL
    qr2xy(q.toInt, r.toInt)
  }

  /**
    * Calculate a hex corner world coordinates.
    *
    * @param corner the corner to calculate.
    * @param cx     the hex center horizontal world location.
    * @param cy     the hex center vertical world location.
    * @return (x,y)
    */
  def cornerOffset(corner: Int, cx: Double, cy: Double): (Double, Double) = {
    (cx + sizeX * orientation.offsetX(corner), cy + sizeY * orientation.offsetY(corner))
  }

  /**
    * Calculate the sequence of the Hex XY corners.
    *
    * @param h the hex.
    * @return sequence of the Hex XY corners.
    */
  def polygon(h: Hex): Iterable[(Double, Double)] = {
    val arr = new ArrayBuffer[(Double, Double)](7)
    val (cx, cy) = hexToXY(h)
    arr += cornerOffset(0, cx, cy)
    arr += cornerOffset(1, cx, cy)
    arr += cornerOffset(2, cx, cy)
    arr += cornerOffset(3, cx, cy)
    arr += cornerOffset(4, cx, cy)
    arr += cornerOffset(5, cx, cy)
    arr += arr.head
  }

}
