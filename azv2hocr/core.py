from html import escape
from string import Template

from .models import VisionResponse


class Annotation:

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
    <meta name='ocr-system' content='azv2hocr' />
    <meta name='ocr-langs' content='$lang' />
    <meta name='ocr-number-of-pages' content='1' />
    <meta name='ocr-capabilities' content='ocr_page ocr_carea ocr_par ocr_line ocrx_word ocrp_lang'/>
  </head>
  <body>
    <div class='ocr_page' lang='$lang' title='image "$image";bbox 0 0 $x1 $y1'>
        $content
    </div>
    <script src="https://unpkg.com/hocrjs"></script>
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
        content=None,
        x0: int = 0,
        y0: int = 0,
        x1: int = 0,
        y1: int = 0,
        image="",
        savefile=False,
    ):
        if content == None:
            self.content = []
        else:
            self.content = content
        self.image = image
        self.htmlid = htmlid
        self.baseline = baseline
        self.lang = lang
        self.ocr_class = ocr_class
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

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


def fromResponse(resp: VisionResponse, file_name: str = "hoge"):
    page = None
    if isinstance(resp, bool) and not resp:
        page = Annotation(ocr_class="ocr_page", htmlid="page_0", title=file_name)
    else:
        for page_no, page_json in enumerate(resp.__root__):
            box = [{"x": 0, "y": 0}, {"x": 0, "y": 0}, {"x": 0, "y": 0}, {"x": 0, "y": 0}]
            page = Annotation(ocr_class="ocr_page", htmlid="page" + str(page_no), x1=1000, y1=1000, image=file_name)
            block = Annotation(ocr_class="ocr_carea", htmlid="block_" + str(page_no), x1=1000, y1=1000)
            page.content.append(block)

            for line_id, line in enumerate(page_json.lines):
                curline = Annotation(
                    ocr_class="ocr_line",
                    htmlid="line_" + str(page_no) + "_" + str(line_id),
                    x0=line.boundingBox[0],
                    y0=line.boundingBox[1],
                    x1=line.boundingBox[4],
                    y1=line.boundingBox[5],
                )

                for word_id, word in enumerate(line.words):
                    word_obj = Annotation(
                        ocr_class="ocrx_word",
                        htmlid="word_" + str(page_no) + "_" + str(line_id) + "_" + str(word_id),
                        content=word.text,
                        x0=word.boundingBox[0],
                        y0=word.boundingBox[1],
                        x1=word.boundingBox[4],
                        y1=word.boundingBox[5],
                    )

                    curline.content.append(word_obj)
                block.content.append(curline)

    return page
