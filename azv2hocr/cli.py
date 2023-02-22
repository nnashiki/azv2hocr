import os

import click
from bs4 import BeautifulSoup

from .core import fromResponse, PdfExtractor
from .models import VisionResponse


@click.group()
@click.option("--main_param_str", required=True, type=str)
@click.option("--main_param_int", required=True, type=int)
@click.option("--main_param_bool", default=False, is_flag=True)
@click.pass_context
def cli(ctx, main_param_bool, main_param_str, main_param_int):
    ctx.ensure_object(dict)
    ctx.obj["MAIN_PARAM_BOOL"] = main_param_bool
    ctx.obj["MAIN_PARAM_STR"] = main_param_str
    ctx.obj["MAIN_PARAM_INT"] = main_param_int


@cli.command()
@click.pass_context
@click.option("--vision_result", type=str)
@click.option("--hocr", type=str)
def convert(ctx, vision_result, hocr):
    click.echo("start convert")
    click.echo(ctx.obj["MAIN_PARAM_BOOL"])
    click.echo(ctx.obj["MAIN_PARAM_STR"])
    click.echo(ctx.obj["MAIN_PARAM_INT"])
    click.echo(vision_result)
    click.echo(hocr)

    vision_response = VisionResponse.parse_file(path=vision_result, content_type="application/json")
    base_path = vision_result.split(".")[0]
    pdf_path = base_path + ".pdf"

    extract_images = []
    with PdfExtractor(pdf_path=pdf_path) as extractor:
        """
        PDF から画像を展開して、Vision API の結果とマッチングさせる
        """
        for file_no, extract_image_file_path in enumerate(extractor.image_file_paths):
            extract_image_file_ext = os.path.basename(extract_image_file_path).split(".")[1]
            out_image_path = base_path + F"_{file_no}." + extract_image_file_ext
            os.rename(extract_image_file_path, out_image_path)   # 画像を work から作業ディレクトリに移動させる
            extract_images.append(os.path.basename(out_image_path))
        hocr_obj = fromResponse(resp=vision_response.__root__, files=extract_images)

    with (open(hocr, "w", encoding="utf-8")) as outfile:
        soup = BeautifulSoup(hocr_obj.render(), "html.parser")
        outfile.write(soup.prettify())
        outfile.close()


if __name__ == "__main__":
    cli(obj={})
