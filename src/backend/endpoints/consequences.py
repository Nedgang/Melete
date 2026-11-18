##########
# IMPORT #
##########
from fastapi import APIRouter

##########
# ROUTER #
##########
router = APIRouter()


################
# CONSEQUENCES #
################
@router.get("/query/v1/consequences")
def find_consequences(variant_type: str, variant_key: str) -> None:
    pass
