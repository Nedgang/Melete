##########
# IMPORT #
##########
import os
from typing import Annotated

import duckdb
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
    chr: str = "",
    start: int = 0,
    stop: int = 0,
    only_pass: bool = False,
    gnomad_regions: bool = False,
    in_gnomad: bool = False,
    pass_gnomad: bool = False,
) -> list[dict]:
    return_dict = {}
    for base in variant_type:
        if os.path.isdir(f"../Mneme/{base}/{chr}"):
            # test = duckdb.sql(f"SELECT * FROM '../Mneme/{base}/{chr}/*.parquet'")
            # print(test.pl().to_dicts())
            base_sql = f"SELECT * FROM '../Mneme/{base}/{chr}/*.parquet'"
            additional_filters = []
            if id != "":
                additional_filters.append(f"id = '{id}'")
            if only_pass:
                additional_filters.append("FILTER = 'PASS'")
            if gnomad_regions:
                additional_filters.append("notCoveredByGnomad = False")
            if in_gnomad:
                additional_filters.append("inGnomad = True")
            if pass_gnomad:
                additional_filters.append("passGnomad = True")

            print(base_sql + f" WHERE {' AND '.join(additional_filters)}")
            if additional_filters == []:
                return_dict[base] = duckdb.sql(base_sql).pl().to_dicts()
            else:
                return_dict[base] = (
                    duckdb.sql(base_sql + f" WHERE {' AND '.join(additional_filters)}")
                    .pl()
                    .to_dicts()
                )
        #     if id != "":
        #         df = df.filter(pl.col("CSQ") == csq)
    return [return_dict]
