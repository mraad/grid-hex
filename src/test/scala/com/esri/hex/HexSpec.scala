package com.esri.hex

import org.scalatest.{FlatSpec, Matchers}

class HexSpec extends FlatSpec with Matchers {

  it should "add" in {
    val h1 = Hex(10, 20, 30)
    val h2 = Hex(11, 22, 33)
    h1 + h2 shouldBe Hex(21, 42, 63)
  }

  it should "sub" in {
    val h1 = Hex(21, 42, 63)
    val h2 = Hex(11, 22, 33)
    h1 - h2 shouldBe Hex(10, 20, 30)
  }

  it should "calc length" in {
    val h1 = Hex(10, -20, 33)
    h1.length shouldBe (10 + 20 + 33) / 2
  }

  it should "range 0" in {
    val h = Hex(10, 20)
    (h range 0).head shouldBe Hex(10, 20)
  }

  it should "range 1" in {
    val h = Hex(10, 20)
    val range = h range 1
    range should contain(h)
    range should contain(h neighbor 0)
    range should contain(h neighbor 1)
    range should contain(h neighbor 2)
    range should contain(h neighbor 3)
    range should contain(h neighbor 4)
    range should contain(h neighbor 5)
  }

  it should "range 2" in {
    val h = Hex(10, 20)
    val range = h range 2
    range.length shouldBe 19
  }
}
