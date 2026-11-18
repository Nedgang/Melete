##########
# IMPORT #
##########
import os
from typing import Annotated

import duckdb
import polars as pl
from fastapi import APIRouter, HTTPException, Query

from src.parameters.variant_selector_columns import variants_columns

##########
# ROUTER #
##########
router = APIRouter()


############
# VARIANTS #
############
@router.get("/query/v1/variants")
def find_variants(
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
) -> dict:
    variant_number_limit = 100000
    answer = {}
    for base in variant_type:
        if os.path.isdir(f"../Mneme/{base}"):
            # Variant selection
            variant_base_sql = (
                f"SELECT DISTINCT {', '.join(variants_columns(base))} "
                + f"FROM '../Mneme/{base}/*.db' WHERE chrom = '{chr}' "
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
                results_df = duckdb.sql(
                    variant_base_sql + f"LIMIT {variant_number_limit} "
                ).pl(lazy=True)
            else:
                results_df = duckdb.sql(
                    variant_base_sql
                    + f" AND {' AND '.join(additional_filters)}"
                    + f"LIMIT {variant_number_limit} "
                ).pl(lazy=True)
            if results_df.select(pl.len()).collect().item() == variant_number_limit:
                answer[base] = {
                    "warning": True,
                    "message": f"""Number of found variants limited to
                    {variant_number_limit} for {base} request.
                    Only the first 100k variants found by your request will be showed.""",
                    "results": results_df.collect().to_dicts(),
                }
            else:
                answer[base] = {
                    "warning": False,
                    "message": "",
                    "results": results_df.collect().to_dicts(),
                }
        else:
            raise HTTPException(status_code=404, detail=f"{base} not found!!!")
    return answer
