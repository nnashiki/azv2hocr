from pydantic import BaseModel
from typing import List


class Style(BaseModel):
    name: str
    confidence: float


class Appearance(BaseModel):
    style: Style


class Word(BaseModel):
    boundingBox: List[int]
    text: str
    confidence: float


class Line(BaseModel):
    boundingBox: List[float]
    appearance: Appearance
    text: str
    words: List[Word]


class ModelItem(BaseModel):
    page: int
    angle: float
    width: int
    height: int
    unit: str
    lines: List[Line]


class VisionResponse(BaseModel):
    __root__: List[ModelItem]
