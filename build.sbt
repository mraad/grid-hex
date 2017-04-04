organization := "com.esri"

name := "grid-hex"

version := "1.0"

isSnapshot := true

publishMavenStyle := true

crossScalaVersions := Seq("2.10.6", "2.11.7")

resolvers += "Local Maven Repository" at "file:///" + Path.userHome + "/.m2/repository"

mainClass in (run) := Some("com.esri.HexApp")

libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.1" % "test"
libraryDependencies += "com.beust" % "jcommander" % "1.64" % "compile"
