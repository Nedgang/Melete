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
def find_consequences() -> None:
    pass
