##########
# IMPORT #
##########
import os

import duckdb
import polars as pl
from fastapi import APIRouter, HTTPException

from src.parameters.consequences_columns import consequence_columns

##########
# ROUTER #
##########
router = APIRouter()


################
# CONSEQUENCES #
################
@router.get("/query/v1/consequences")
def find_consequences(variant_type: str, variant_key: str) -> dict:
    if os.path.isdir(f"../Mneme/{variant_type}"):
        return {
            "warning": False,
            "message": "",
            "results": duckdb.sql(
                f"SELECT {', '.join(consequence_columns(variant_type))} "
                + f"FROM '../Mneme/{variant_type}/*.db' "
                + f"WHERE variant_key = '{variant_key}' "
            )
            .pl(lazy=True)
            .collect()
            .to_dicts(),
        }
    else:
        raise HTTPException(status_code=404, detail=f"{variant_type} not found!!!")
