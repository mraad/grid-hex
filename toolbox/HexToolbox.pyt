import os

import arcpy
import glob
import pyarrow.parquet as pq  # pip install pyarrow
from gridhex import Hex, Layout
from pathlib import Path


class Toolbox(object):
    def __init__(self):
        self.label = "HexToolbox"
        self.alias = "HexToolbox"
        self.tools = [ImportTextTool, ImportParquetTool]


class ImportTextTool(object):
    def __init__(self):
        self.label = "Import Hex Text"
        self.description = "Read Hex aggregations from text files."
        self.canRunInBackground = True

    def getParameterInfo(self):
        out_fc = arcpy.Parameter(
            name="out_fc",
            displayName="out_fc",
            direction="Output",
            datatype="Feature Layer",
            parameterType="Derived")

        in_path = arcpy.Parameter(
            name="in_path",
            displayName="Hex Bin File",
            direction="Input",
            datatype=["DEFile", "DEFolder"],
            parameterType="Required")

        in_name = arcpy.Parameter(
            name="in_name",
            displayName="Name",
            direction="Input",
            datatype="GPString",
            parameterType="Required")
        in_name.value = "Hex100"

        in_size = arcpy.Parameter(
            name="in_size",
            displayName="Hex Size",
            direction="Input",
            datatype="GPDouble",
            parameterType="Required")
        in_size.value = 100.0

        return [out_fc, in_path, in_name, in_size]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        arcpy.env.autoCancelling = False

        p_path = parameters[1].valueAsText
        p_name = parameters[2].value
        p_size = parameters[3].value

        if os.path.isdir(p_path):
            p_path = os.path.join(p_path, "part-*")
        g_files = glob.glob(p_path)
        g_files = [g_file for g_file in g_files if os.path.getsize(g_file) > 0]
        if len(g_files) == 0:
            arcpy.AddError("Cannot find non empty file(s) that match '{}'".format(p_path))
            return

        # ws = arcpy.env.scratchGDB
        ws = "memory"
        fc = os.path.join(ws, p_name)
        if arcpy.Exists(fc):
            arcpy.management.Delete(fc)

        spatial_reference = arcpy.SpatialReference(3857)
        arcpy.management.CreateFeatureclass(ws,
                                            p_name,
                                            "POLYGON",
                                            spatial_reference=spatial_reference,
                                            has_m="DISABLED",
                                            has_z="DISABLED")
        arcpy.management.AddField(fc, "POP", "LONG")

        layout = Layout(p_size, Layout.top_flat)
        with arcpy.da.InsertCursor(fc, ["SHAPE@", "POP"]) as cursor:
            for p_file in g_files:
                if arcpy.env.isCancelled:
                    break
                with open(p_file, "r") as f:
                    for line in f:
                        row = line.rstrip("\n").split("\t")
                        row[0] = Hex.from_nume(int(row[0])).to_coords(layout)
                        cursor.insertRow(row)
        symbology = Path(__file__).parent / f"{p_name}.lyrx"
        if symbology.exists():
            parameters[0].symbology = str(symbology)
        parameters[0].value = fc


class ImportParquetTool(object):
    def __init__(self):
        self.label = "Import Hex Parquet"
        self.description = "Read Hex aggregations from parquet files."
        self.canRunInBackground = True

    def getParameterInfo(self):
        out_fc = arcpy.Parameter(
            name="out_fc",
            displayName="out_fc",
            direction="Output",
            datatype="Feature Layer",
            parameterType="Derived")

        in_folder = arcpy.Parameter(
            name="in_folder",
            displayName="Parquet Folder",
            direction="Input",
            datatype="DEFolder",
            parameterType="Required")

        in_name = arcpy.Parameter(
            name="in_name",
            displayName="Output Layer Name",
            direction="Input",
            datatype="GPString",
            parameterType="Required")
        in_name.value = "Hex100"

        in_field = arcpy.Parameter(
            name="in_field",
            displayName="Hex Field",
            direction="Input",
            datatype="GPString",
            parameterType="Required")
        in_field.value = "hex100"

        in_size = arcpy.Parameter(
            name="in_size",
            displayName="Hex Meters",
            direction="Input",
            datatype="GPDouble",
            parameterType="Required")
        in_size.value = 100.0

        return [out_fc,
                in_name,
                in_folder,
                in_field,
                in_size
                ]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        p_name = parameters[1].value
        p_path = parameters[2].valueAsText
        p_field = parameters[3].value
        p_size = parameters[4].value

        layout = Layout(p_size, Layout.top_flat)

        p = Path(p_path)
        parts = list(p.glob('part-*'))
        if len(parts) == 0:
            arcpy.AddError(f"No part files in {p_path}.")
            return

        ws = "memory"  # arcpy.env.scratchGDB
        fc = os.path.join(ws, p_name)
        if arcpy.Exists(fc):
            arcpy.management.Delete(fc)

        sp_ref = arcpy.SpatialReference(3857)
        arcpy.management.CreateFeatureclass(
            ws,
            p_name,
            "POLYGON",
            spatial_reference=sp_ref,
            has_m="DISABLED",
            has_z="DISABLED")
        ap_fields = ["SHAPE@"]
        pq_fields = [p_field]
        with open(parts[0], 'rb') as f:
            table = pq.read_table(f)
            schema = table.schema
            for field in schema:
                if field.name != p_field:
                    f_name = field.name
                    f_type = str(field.type)
                    arcpy.AddMessage(f"{f_name} {f_type}")
                    a_type = {
                        'int32': 'INTEGER',
                        'int64': 'LONG',
                        'float': 'DOUBLE',
                        'double': 'DOUBLE'
                    }.get(f_type, 'TEXT')
                    arcpy.management.AddField(fc, f_name, a_type, field_length=256)
                    ap_fields.append(f_name)
                    pq_fields.append(f_name)

        arcpy.env.autoCancelling = False
        with arcpy.da.InsertCursor(fc, ap_fields) as cursor:
            nume = 0
            for p_file in parts:
                if arcpy.env.isCancelled:
                    break
                with open(str(p_file), 'rb') as f:
                    table = pq.read_table(f)
                    pydict = table.to_pydict()
                    for i in range(table.num_rows):
                        row = [pydict[c][i] for c in pq_fields]
                        row[0] = Hex.from_nume(row[0]).to_coords(layout)
                        cursor.insertRow(row)
                        nume += 1
                        if nume % 1000 == 0:
                            arcpy.SetProgressorLabel(f"Inserted {nume} Features...")
                            if arcpy.env.isCancelled:
                                break
            arcpy.SetProgressorLabel(f"Inserted {nume} Features.")
        symbology = Path(__file__).parent / f"{p_name}.lyrx"
        if symbology.exists():
            parameters[0].symbology = str(symbology)
        parameters[0].value = fc
        arcpy.ResetProgressor()