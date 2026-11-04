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
        if os.path.isdir(f"../Mneme/{base}"):
            # Variant selection
            variant_base_sql = (
                f"SELECT * FROM '../Mneme/{base}/*.db' WHERE chrom = '{chr}'"
            )
            additional_filters = []
            # Filters on the variant info
            if id != "":
                additional_filters.append(f"id = '{id}'")
            if only_pass:
                additional_filters.append("FILTER = 'PASS'")
            if start != 0 or stop != 0:
                additional_filters.append(f"pos BETWEEN {start} AND {stop}")
            # Those are linked, use the biggest one instead of multiple at the same time.
            # Filters on the variant link to gnomAD
            if pass_gnomad:
                additional_filters.append("passGnomad = True")
            elif in_gnomad:
                additional_filters.append("inGnomad = True")
            elif gnomad_regions:
                additional_filters.append("notCoveredByGnomad = False")
            # Filter on CSQ informations
            if csq is not None:
                additional_filters.append(
                    f"csq_Consequence IN {tuple([i.strip() for i in csq])}"
                )
            if impact is not None:
                additional_filters.append(
                    f"csq_IMPACT IN {tuple([i.strip() for i in impact])}"
                )
            if feature is not None:
                additional_filters.append(
                    f"csq_Feature IN {tuple([i.strip() for i in feature])}"
                )
            if gene != "":
                additional_filters.append(f"csq_SYMBOL = '{gene.strip()}'")

            # Complete the basic request with additional filters
            if additional_filters == []:
                results_df = duckdb.sql(variant_base_sql).pl()
            else:
                results_df = duckdb.sql(
                    variant_base_sql + f" AND {' AND '.join(additional_filters)}"
                ).pl()
            # Check if results are in line with the limit of data.
            if len(results_df) > 100000:
                raise HTTPException(
                    status_code=403,
                    detail=f"Request too open-ended, number of results > 100000 in {base} request.",
                )
            else:
                return_dict[base] = results_df.to_dicts()

        else:
            return_dict[base] = {}
    return [return_dict]
