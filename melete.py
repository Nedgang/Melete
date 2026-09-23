##########
# IMPORT #
##########
from typing import Annotated

import polars as pl
from fastapi import FastAPI, Query

########
# MAIN #
########
app = FastAPI()


#############
# FUNCTIONS #
#############
@app.get("/query/")
async def read_items(
    variant_type: Annotated[list[str] | None, Query()],
    csq: Annotated[list[str] | None, Query()] = None,
    id: str = "",
    gene: str = "",
    chr: int = 0,
    start: int = 0,
    stop: int = 0,
    only_pass: bool = False,
    gnomad_regions: bool = False,
    in_gnomad: bool = False,
    pass_gnomad: bool = False,
) -> list[dict]:
    return_dict = {}
    for base in variant_type:
        df = pl.scan_parquet(f"./test_dataset/{base}_chr{chr}.parquet")
        if id != "":
            df = df.filter(pl.col("id") == id)
        if csq is not None:
            df = df.filter(pl.col("CSQ") == csq)
        if only_pass:
            df = df.filter(pl.col("filter") == "PASS")
        # if gnomad_regions:
        #     df = df.filter(pl.col("notCoveredByGnomad") == False)
        if in_gnomad:
            df = df.filter(pl.col("in_gnomAD") == True)
        if pass_gnomad:
            df = df.filter(pl.col("pass_gnomad") == True)
        return_dict[base] = df.collect().to_dicts()
    return [return_dict]
