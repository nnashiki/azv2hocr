from pydantic import BaseModel
from typing import List

inch = 72.0


class Style(BaseModel):
    name: str
    confidence: float


class Appearance(BaseModel):
    style: Style


class Word(BaseModel):
    boundingBox: List[float]
    text: str
    confidence: float


class Line(BaseModel):
    boundingBox: List[float]
    appearance: Appearance
    text: str
    words: List[Word]


class Page(BaseModel):
    page: int
    angle: float
    width: float
    height: float
    unit: str
    lines: List[Line]


class VisionResponse(BaseModel):
    __root__: List[Page]


def inch_to_pixel_converter(page: Page) -> Page:
    """
    Convert inch to pixel
    """
    if page.unit == "inch":
        page.width = int(page.width * inch)
        page.height = int(page.height * inch)
        for line in page.lines:
            line.boundingBox = [int(x * inch) for x in line.boundingBox]
            for word in line.words:
                word.boundingBox = [int(x * inch) for x in word.boundingBox]
    return page
