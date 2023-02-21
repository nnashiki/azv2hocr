from pydantic import BaseModel


class Style(BaseModel):
    name: str
    confidence: float


class Appearance(BaseModel):
    style: Style


class Word(BaseModel):
    boundingBox: list[int]
    text: str
    confidence: float


class Line(BaseModel):
    boundingBox: list[float]
    appearance: Appearance
    text: str
    words: list[Word]


class ModelItem(BaseModel):
    page: int
    angle: float
    width: float
    height: float
    unit: str
    lines: list[Line]


class VisionResponse(BaseModel):
    __root__: list[ModelItem]
