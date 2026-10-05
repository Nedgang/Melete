##########
# IMPORT #
##########
import os
from typing import Annotated

import duckdb
import polars as pl
from fastapi import FastAPI, Query, HTTPException

########
# MAIN #
########
app = FastAPI()


#############
# FUNCTIONS #
#############
@app.get("/query/v1/variants")
async def find_variants(
    variant_type: Annotated[list[str] | None, Query()],
    chr: str,
    csq: Annotated[list[str] | None, Query()] = None,
    id: str = "",
    impact: Annotated[list[str] | None, Query()] = None,
    feature: Annotated[list[str] | None, Query()] = None,
    gene: str = "",
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
            # Variant selection
            variant_base_sql = f"FROM '../Mneme/{base}/{chr}/variants/*.parquet'"
            additional_filters = []
            if id != "":
                additional_filters.append(f"id = '{id}'")
            if only_pass:
                additional_filters.append("FILTER = 'PASS'")
            if start != 0 and stop != 0:
                additional_filters.append(f"pos BETWEEN {start} AND {stop}")
            # Those are linked, use the bigger one instead of multiple at the same time.
            if pass_gnomad:
                additional_filters.append("passGnomad = True")
            elif in_gnomad:
                additional_filters.append("inGnomad = True")
            elif gnomad_regions:
                additional_filters.append("notCoveredByGnomad = False")

            if additional_filters == []:
                variant_request = variant_base_sql
            else:
                variant_request = (
                    variant_base_sql + f" WHERE {' AND '.join(additional_filters)}"
                )

            if (
                csq is not None
                or impact is not None
                or feature is not None
                or gene != ""
            ):
                csq_base_request = f"SELECT DISTINCT variant_key FROM '../Mneme/{base}/{chr}/csq/*.parquet' WHERE variant_key IN (SELECT variant_key {variant_request})"
                additional_filters = []
                if csq is not None:
                    additional_filters.append(
                        f"Consequence IN {tuple([i.strip() for i in csq])}"
                    )
                if impact is not None:
                    additional_filters.append(
                        f"IMPACT IN {tuple([i.strip() for i in impact])}"
                    )
                if feature is not None:
                    additional_filters.append(
                        f"Feature IN {tuple([i.strip() for i in feature])}"
                    )
                if gene != "":
                    additional_filters.append(f"SYMBOL = '{gene.strip()}'")

                results_df = (
                    duckdb.sql(
                        "SELECT * FROM '../Mneme/"
                        + base
                        + "/"
                        + chr
                        + "/variants/*.parquet' WHERE variant_key IN ("
                        + csq_base_request
                        + f" AND {' AND '.join(additional_filters)}"
                        + ")"
                    )
                    .pl()
                    .with_columns(
                        pl.col(["AF", "AF_XY", "AF_XX", "AF_grpmax"]).round(4)
                    )
                )
            else:
                results_df = (
                    duckdb.sql(f"SELECT * {variant_request}")
                    .pl()
                    .with_columns(
                        pl.col(["AF", "AF_XY", "AF_XX", "AF_grpmax"]).round(4)
                    )
                )
            # Check if results are in line with the limit of data.
            if len(results_df) > 200:
                raise HTTPException(
                    status_code=403,
                    detail=f"Request too open-ended, number of results > 200 in {base} request.",
                )
            else:
                return_dict[base] = results_df.to_dicts()

        else:
            return_dict[base] = {}
    return [return_dict]


@app.get("/query/v1/csq")
async def find_csq(
    variant_type: str,
    chr: str,
    variant_key: str,
    features: Annotated[list[str] | None, Query()] = None,
) -> list[dict]:
    if os.path.isdir(f"../Mneme/{variant_type}/{chr}"):
        request = f"SELECT * FROM '../Mneme/{variant_type}/{chr}/csq/*.parquet' WHERE variant_key = '{variant_key}'"
        if features is not None:
            request = (
                request + f" AND Feature IN {tuple([i.strip() for i in features])}"
            )
        return duckdb.sql(request).pl().to_dicts()
    else:
        return [{}]
