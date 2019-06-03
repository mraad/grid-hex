package com.esri.hex;

import com.beust.jcommander.Parameter;

/**
 * The arguments for the HexApp application.
 */
class HexAppArgs
{
    /**
     * Print usage.
     */
    @Parameter(names = {"-help"}, description = "Print usage")
    boolean printUsage = false;
    /**
     * The output image width.
     */
    @Parameter(names = {"-imgW", "-w"}, description = "Image width")
    int imgW = 400;

    /**
     * The output image height.
     */
    @Parameter(names = {"-imgH", "-h"}, description = "Image height")
    int imgH = 400;

    /**
     * The hex horizontal size.
     */
    @Parameter(names = {"-sizeX"}, description = "Hex horizontal size")
    double sizeX = 20.0;

    /**
     * The hex vertical size.
     */
    @Parameter(names = {"-sizeY"}, description = "Hex vertical size")
    int sizeY = 20;

    /**
     * The point horizontal location to range around.
     */
    @Parameter(names = {"-x"}, description = "Point horizontal location")
    int x = 140;

    /**
     * The point vertical location to range around.
     */
    @Parameter(names = {"-y"}, description = "Point vertical location")
    int y = 160;

    /**
     * The range count.
     */
    @Parameter(names = {"-range", "-r"}, description = "Search range")
    int range = 1;

    /**
     * The PNG file output path.
     */
    @Parameter(names = {"--output-file", "-o", "-f"}, description = "PNG file output path")
    String path = "/tmp/hex.png";

}
