# python-cli-app-skeleton
azv2hocr converts from Azure Computer Vision OCR output to hocr to make a searchable pdf.

# set up

``` shell
poetry env use 3.8
poetry shell
poetry install
```

``` shell
$ poetry run azv2hocr --main_param_str hoge --main_param_int 1 convert --vision_result sample/handwriting.json --hocr sample/handwriting.html
$ poetry run azv2hocr --main_param_str hoge --main_param_int 1 convert --vision_result sample-single-pdf/sample-single.json --hocr sample-single-pdf/sample-single.html
```

``` shell
start sub
False
hoge
1
fuga
```
