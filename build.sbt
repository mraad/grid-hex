organization := "com.esri"

name := "grid-hex"

version := "1.1"

isSnapshot := true

publishMavenStyle := true

crossScalaVersions := Seq("2.10.6", "2.11.7")

resolvers += "Local Maven Repository" at "file:///" + Path.userHome + "/.m2/repository"

mainClass in (run) := Some("com.esri.HexApp")

libraryDependencies ++= Seq(
  "org.scalatest" %% "scalatest" % "3.0.1" % "test",
  "com.beust" % "jcommander" % "1.64" % "compile"
)

pomExtra :=
  <url>https://github.com/mraad/grid-hex</url>
    <licenses>
      <license>
        <name>Apache License, Verision 2.0</name>
        <url>http://www.apache.org/licenses/LICENSE-2.0.html</url>
        <distribution>repo</distribution>
      </license>
    </licenses>
    <scm>
      <url>git@github.com:mraad/grid-hex.git</url>
      <connection>scm:git:git@github.com:mraad/grid-hex.git</connection>
    </scm>
    <developers>
      <developer>
        <id>mraad</id>
        <name>Mansour Raad</name>
        <url>https://github.com/mraad</url>
        <email>mraad@esri.com</email>
      </developer>
    </developers>
