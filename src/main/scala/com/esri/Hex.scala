package com.esri

import scala.collection.mutable.ArrayBuffer
import scala.math._

/**
  * Class to represent a Hex Cube.
  *
  * @param q the column component.
  * @param r the row component.
  * @param s the z component.
  */
case class Hex(q: Int, r: Int, s: Int) extends Ordered[Hex] {

  /**
    * Add this Hex to another Hex.
    *
    * @param that the Hex to add.
    * @return a new Hex instance with component sum.
    */
  def +(that: Hex) = {
    Hex(this.q + that.q, this.r + that.r, this.s + that.s)
  }

  /**
    * Subtract a given hex from this Hex.
    *
    * @param that the hex to subtract.
    * @return a new Hex instance with component difference.
    */
  def -(that: Hex) = {
    Hex(this.q - that.q, this.r - that.r, this.s - that.s)
  }

  /**
    * Find a Hex neighbor given a direction.
    *
    * @param dir the direction of the neighbor. Should be [0 and 5].
    * @return the hex neighbor.
    */
  def neighbor(dir: Int) = {
    // TODO Assert dir in [0 to 5]
    this + Hex.neighborArr(dir)
  }

  /**
    * Calculate the manhattan distance of this Hex.
    *
    * @return the manhattan distance.
    */
  def length() = {
    (abs(q) + abs(r) + abs(s)) / 2
  }

  /**
    * Calculate the manhattan distance to a given Hex.
    *
    * @param that the Hex to calculate the distance to.
    * @return the manhattan distance.
    */
  def distance(that: Hex) = {
    (that - this).length
  }

  /**
    * Calculate the sequence of the Hex XY corners.
    *
    * @param layout implicit grid layout.
    * @return sequence of hex XY corners.
    */
  def polygon()(implicit layout: Layout): Iterable[(Double, Double)] = {
    layout polygon this
  }

  /**
    * Calc XY center of this Hex.
    *
    * @param layout implicit grid layout.
    * @return the XY center.
    */
  def toXY()(implicit layout: Layout): (Double, Double) = {
    layout hexToXY this
  }

  /**
    * Find sequence of hexes that are within a given range.
    *
    * @param n the range.
    * @return sequence of hexes that are within a given range.
    */
  def range(n: Int): Seq[Hex] = {
    // TODO Assert n >= 0
    n match {
      case 0 => Seq(this)
      case _ =>
        val arr = new ArrayBuffer[Hex](7 * n)
        val nn = -n
        var dq = nn
        while (dq <= n) {
          val rmax = n.min(-dq + n)
          var dr = nn.max(-dq - n)
          while (dr <= rmax) {
            val ds = -dq - dr
            arr += Hex(q + dq, r + dr, s + ds)
            dr += 1
          }
          dq += 1
        }
        arr
    }
  }

  /**
    * Compare this q/r to that q/r
    *
    * @param that the Hex to compare with.
    * @return -1 if less, 1 if greater, 0 otherwise.
    */
  override def compare(that: Hex): Int = {
    this.q compare that.q match {
      case 0 => this.r compare that.r
      case c => c
    }
  }
}

object Hex extends Serializable {
  private val neighborArr = Array(
    Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)
  )

  /**
    * Create a Hex given a column and a row. Hex cube coordinates have to sum (q+r+s) to 0
    *
    * @param q the column.
    * @param r the row.
    * @return Hex(q,r,-q-r)
    */
  def apply(q: Int, r: Int): Hex = new Hex(q, r, -q - r)

  /**
    * Create a Hex given a layout x and y coodinates.
    *
    * @param x      the layout x coordinate.
    * @param y      the layout y coordinate.
    * @param layout implicit grid layout.
    * @return a Hex instance.
    */
  def fromXY(x: Double, y: Double)(implicit layout: Layout): Hex = layout.xyToHex(x, y).toHex
}
