package com.esri.hex

import scala.math._

/**
  * Class to represent a Hex with components in double format.
  *
  * @param q the column component.
  * @param r the row component.
  * @param s the cube s or z component.
  */
case class FractionalHex(q: Double, r: Double, s: Double) {

  /**
    * Convert to Hex instance by rounding.
    *
    * @return a rounded Hex instance.
    */
  def toHex(): Hex = {
    var qInt = q.round.toInt
    var rInt = r.round.toInt
    var sInt = s.round.toInt

    val qAbs = abs(qInt - q)
    val rAbs = abs(rInt - r)
    val sAbs = abs(sInt - s)

    if (qAbs > rAbs && qAbs > sAbs) qInt = -rInt - sInt
    else if (rAbs > sAbs) rInt = -qInt - sInt
    else sInt = -qInt - rInt

    Hex(qInt, rInt, sInt)
  }

}
