package com.esri

import java.awt.image.BufferedImage
import java.awt.{Color, Graphics2D, RenderingHints}
import java.io.FileOutputStream
import javax.imageio.ImageIO

import com.beust.jcommander.JCommander

/**
  * Simple app to help in visualizing world to hex conversion and range calculation.
  * The output is a PNG image.
  */
object HexApp extends App {

  System.setProperty("java.awt.headless", "true")

  val appParam = new HexAppArgs()
  val jc = new JCommander(appParam, args.toArray: _*)
  if (appParam.printUsage) {
    jc.usage()
    System.exit(0)
  }

  val bi = new BufferedImage(appParam.imgW, appParam.imgH, BufferedImage.TYPE_INT_RGB)

  implicit val layout = Layout(bi.getWidth / 2, bi.getHeight / 2, appParam.sizeX, appParam.sizeY)

  val hex = Hex.fromXY(appParam.x, appParam.y)

  val g = bi.getGraphics.asInstanceOf[Graphics2D]
  try {
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
    g.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY)
    g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE)
    g.setRenderingHint(RenderingHints.KEY_COLOR_RENDERING, RenderingHints.VALUE_COLOR_RENDER_QUALITY)

    g.setBackground(Color.LIGHT_GRAY)
    g.clearRect(0, 0, bi.getWidth, bi.getHeight)

    g.setColor(Color.DARK_GRAY)
    g.drawLine(0, bi.getHeight / 2, bi.getWidth, bi.getHeight / 2)
    g.drawLine(bi.getWidth / 2, 0, bi.getWidth / 2, bi.getHeight)

    def drawPoly(poly: Iterable[(Double, Double)]) = {
      poly
        .sliding(2)
        .foreach(pq => {
          val (px, py) = pq.head
          val (qx, qy) = pq.last
          g.drawLine(px.toInt, py.toInt, qx.toInt, qy.toInt)
        })
    }

    g.setColor(Color.BLUE)
    hex
      .range(appParam.range)
      .foreach(h => drawPoly(h.polygon))

    g.setColor(Color.RED)
    g.fillOval(appParam.x - 6 / 2, appParam.y - 6 / 2, 6, 6)
    drawPoly(hex.polygon)

  } finally {
    g.dispose()
  }
  val outputStream = new FileOutputStream(appParam.path)
  try {
    ImageIO.write(bi, "png", outputStream)
  } finally {
    outputStream.close()
  }

}
