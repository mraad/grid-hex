package com.esri

import org.scalatest.{FlatSpec, Matchers}

class LayoutSpec extends FlatSpec with Matchers {

  it should "hexToPixel pixelToHex" in {
    val layout = Layout(10, 20, 100, 100, Orientation.TOP_FLAT)
    val (px, py) = layout.hexToXY(Hex(10, 20))
    val hex = layout.xyToHex(px, py).toHex
    hex.q shouldBe 10
    hex.r shouldBe 20
    hex.s shouldBe -30
  }

  it should "work on web coordinates" in {
    implicit val layout = Layout(0.0, 0.0, 1000, 1000, Orientation.TOP_FLAT)

  }

  it should "work on geo coordinates" in {
    implicit val layout = Layout(0.0, 0.0, 1, 1, Orientation.TOP_FLAT)

    Seq(
      (-180.0, -90.0),
      (-90.0, -45.0),
      (0.0, 0.0),
      (90.0, 45.0),
      (180.0, 90.0)
    )
      .foreach {
        case (lon, lat) => {
          val hex = Hex.fromXY(lon, lat)
          val (x, y) = hex.toXY()
          x shouldBe lon +- 0.1
          y shouldBe lat +- 0.1
        }
      }
  }
}
