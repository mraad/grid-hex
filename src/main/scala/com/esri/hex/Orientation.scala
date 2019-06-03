package com.esri.hex

import scala.math._

/**
  * Class to define the hex orientation, either flat top or pointy top.
  */
case class Orientation(
                        f0: Double, f1: Double, f2: Double, f3: Double,
                        b0: Double, b1: Double, b2: Double, b3: Double,
                        startAngle: Double
                      ) {
  private val Pi_over_3 = Pi / 3.0
  val offsetX = Array(
    cos(Pi_over_3 * (startAngle - 0)),
    cos(Pi_over_3 * (startAngle - 1)),
    cos(Pi_over_3 * (startAngle - 2)),
    cos(Pi_over_3 * (startAngle - 3)),
    cos(Pi_over_3 * (startAngle - 4)),
    cos(Pi_over_3 * (startAngle - 5))
  )
  val offsetY = Array(
    sin(Pi_over_3 * (startAngle - 0)),
    sin(Pi_over_3 * (startAngle - 1)),
    sin(Pi_over_3 * (startAngle - 2)),
    sin(Pi_over_3 * (startAngle - 3)),
    sin(Pi_over_3 * (startAngle - 4)),
    sin(Pi_over_3 * (startAngle - 5))
  )
}

object Orientation {
  val TOP_FLAT = Orientation(3.0 / 2.0, 0.0, sqrt(3.0) / 2.0, sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0, sqrt(3.0) / 3.0, 0.0)
  val TOP_POINTY = Orientation(sqrt(3.0), sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
}
