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

    with (open(vision_result, "r", encoding="utf-8")) as infile:
        vision_response = VisionResponse.parse_file(path=vision_result, content_type="application/json")
        files = os.path.basename(vision_result).split(".")
        file_name = files[0]
        print(f"file_name: {file_name}")
        file_ext = files[1]
        print(f"file_ext: {file_ext}")

        pdf_path = vision_result.split(".")[0] + ".pdf"
        extract_images = []
        with PdfExtractor(pdf_path=pdf_path) as extractor:
            for file_no, file in enumerate(extractor.image_file_paths):
                out_image_path = vision_result.split(".")[0] + F"_{file_no}." + os.path.basename(file).split(".")[1]
                os.rename(file, out_image_path)
                extract_images.append(os.path.basename(out_image_path))
            hocr_obj = fromResponse(resp=vision_response.__root__, files=extract_images)

        infile.close()

    with (open(hocr, "w", encoding="utf-8")) as outfile:
        soup = BeautifulSoup(hocr_obj.render(), "html.parser")
        outfile.write(soup.prettify())
        outfile.close()


if __name__ == "__main__":
    cli(obj={})
