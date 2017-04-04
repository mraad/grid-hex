package com.esri

import org.scalatest.{FlatSpec, Matchers}

class LayoutSpec extends FlatSpec with Matchers {

  it should "hexToPixel pixelToHex" in {
    val layout = Layout(100, 100, 10, 20, Orientation.TOP_FLAT)
    val (px, py) = layout.hexToXY(Hex(10, 20))
    val hex = layout.xyToHex(px, py).toHex
    hex.q shouldBe 10
    hex.r shouldBe 20
    hex.s shouldBe -30
  }
}
