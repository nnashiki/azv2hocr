import argparse
import json
import sys
from html import escape
from string import Template


class GCVAnnotation:

    height = None
    width = None

    templates = {
        "ocr_page": Template(
            """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="$lang" lang="$lang">
  <head>
    <title>HOCR File</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <meta name='ocr-system' content='gcv2hocr.py' />
    <meta name='ocr-langs' content='$lang' />
    <meta name='ocr-number-of-pages' content='1' />
    <meta name='ocr-capabilities' content='ocr_page ocr_carea ocr_par ocr_line ocrx_word ocrp_lang'/>
  </head>
  <body>
    <div class='ocr_page' lang='$lang' title='image "$title";bbox 0 0 $page_width $page_height'>
        <div class='ocr_carea' lang='$lang' title='bbox $x0 $y0 $x1 $y1'>$content</div>
    </div>
  </body>
</html>
    """
        ),
        "ocr_line": Template(
            """
            <span class='ocr_line' id='$htmlid' title='bbox $x0 $y0 $x1 $y1; baseline $baseline'>$content
            </span>"""
        ),
        "ocrx_word": Template(
            """
                <span class='ocrx_word' id='$htmlid' title='bbox $x0 $y0 $x1 $y1'>$content</span>"""
        ),
        "ocr_carea": Template(
            """
                <div class='ocr_carea' id='$htmlid' title='bbox $x0 $y0 $x1 $y1'>$content</div>"""
        ),
        "ocr_par": Template(
            """
                <p class='ocr_par' dir='ltr' id='$htmlid' title='bbox $x0 $y0 $x1 $y1'>$content</p>"""
        ),
    }

    def __init__(
        self,
        htmlid=None,
        ocr_class=None,
        lang="unknown",
        baseline="0 0",
        page_height=None,
        page_width=None,
        content=None,
        box=None,
        title="",
        savefile=False,
    ):
        if content == None:
            self.content = []
        else:
            self.content = content
        self.title = title
        self.htmlid = htmlid
        self.baseline = baseline
        self.page_height = GCVAnnotation.height if GCVAnnotation.height else page_height
        self.page_width = GCVAnnotation.width if GCVAnnotation.width else page_width
        self.lang = lang
        self.ocr_class = ocr_class
        try:
            self.x0 = int(float(self.page_width * (box[0]["x"] if "x" in box[0] and box[0]["x"] > 0 else 0)))
            self.y0 = int(float(self.page_height * (box[0]["y"] if "y" in box[0] and box[0]["y"] > 0 else 0)))
            self.x1 = int(float(self.page_width * (box[2]["x"] if "x" in box[2] and box[2]["x"] > 0 else 0)))
            self.y1 = int(float(self.page_height * (box[2]["y"] if "y" in box[2] and box[2]["y"] > 0 else 0)))
        except ValueError as e:
            output = (
                "Input JSON does not have proper boundingBox values. "
                "This page of the PDF either must not have been "
                "parsed correctly by GCV or the JSON is somehow corrupt."
            )
            print(e, "\n", output)

    def maximize_bbox(self):
        self.x0 = min([w.x0 for w in self.content])
        self.y0 = min([w.y0 for w in self.content])
        self.x1 = max([w.x1 for w in self.content])
        self.y1 = max([w.y1 for w in self.content])

    def __repr__(self):
        return "<%s [%s %s %s %s]>%s</%s>" % (
            self.ocr_class,
            self.x0,
            self.y0,
            self.x1,
            self.y1,
            self.content,
            self.ocr_class,
        )

    def render(self):
        if type(self.content) == type([]):
            content = "".join(map(lambda x: x.render(), self.content))
        else:
            content = escape(self.content)
        return self.__class__.templates[self.ocr_class].substitute(self.__dict__, content=content)
