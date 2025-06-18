import fastapi as FastApi
from pydantic import BaseModel


class PredHou(BaseModel):
    road_access: float
    facing: str
    parking: float
    bathroom: int
    location: str
    land_area_sq_m: float
    bhk: int