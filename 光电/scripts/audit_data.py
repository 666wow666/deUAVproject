"""Inspect actual files without interpreting unknown height semantics."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
import geopandas as gpd
import numpy as np
from optical_model import load_buildings

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset",type=Path,help="directory containing 区域数据 and the two DOC files")
    p.add_argument("--pdf",type=Path)
    p.add_argument("--output",type=Path,default=ROOT/"outputs/data_audit.json")
    args=p.parse_args()
    base=args.dataset
    shp=base/"区域数据/building/zheng_apart.shp"
    scene=load_buildings(shp)
    gdf=gpd.read_file(shp)
    h=gdf["high"]
    report={"building":scene.audit,
            "high_observations":{"min":float(h.min()),"max":float(h.max()),"null":int(h.isna().sum()),"nonpositive":int((h<=0).sum()),"unique":int(h.nunique()),"semantics":"unknown; not automatically used as height"},
            "source_files":[]}
    for path in sorted(base.rglob("*")):
        if path.is_file():
            entry={"path":str(path.relative_to(base)),"bytes":path.stat().st_size}
            # Data provenance fingerprints, not access to any unrelated files.
            entry["sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
            report["source_files"].append(entry)
    if args.pdf:
        report["pdf"]={"path":str(args.pdf),"sha256":hashlib.sha256(args.pdf.read_bytes()).hexdigest()}
    try:
        import rasterio
        with rasterio.open(base/"区域数据/dem/dem.tif") as ds:
            arr=ds.read(1,masked=True)
            report["dem"]={"crs":str(ds.crs),"width":ds.width,"height":ds.height,"count":ds.count,
                           "dtype":ds.dtypes,"nodata":ds.nodata,"bounds":list(ds.bounds),
                           "pixel_size":list(ds.res),"band_units":ds.units,
                           "min":float(arr.min()),"max":float(arr.max()),"valid_pixels":int(arr.count()),
                           "vertical_datum":"unknown; dataset description calls this ground altitude; no joint datum verification"}
    except ImportError:
        report["dem"]={"state":"not_read","reason":"optional rasterio not installed"}
    tiles=json.loads((base/"区域数据/白模/zhengzhou1/tileset.json").read_text(encoding="utf-8"))
    report["white_model"]={"asset":tiles["asset"],"properties":tiles.get("properties"),
                           "root_transform":tiles["root"]["transform"],
                           "content":[c["content"]["uri"] for c in tiles["root"]["children"]],
                           "scope":"metadata only; GLB geometry not reconstructed or used as verified height"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="source_files"},ensure_ascii=True,indent=2))

if __name__=="__main__":main()
