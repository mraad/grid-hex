organization := "com.esri"

name := "grid-hex"

version := "2.2"

isSnapshot := true

publishMavenStyle := true

crossScalaVersions := Seq("2.10.6", "2.11.12", "2.12.8")

resolvers += Resolver.mavenLocal

mainClass in (run) := Some("com.esri.hex.HexApp")

libraryDependencies ++= Seq(
  "org.scalatest" %% "scalatest" % "3.0.4" % "test",
  "com.beust" % "jcommander" % "1.78" % "compile,runtime"
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
