import click


@click.group()
@click.option("--main_param_str", required=True, type=str)
@click.option("--main_param_int", required=True, type=int)
@click.option('--main_param_bool', default=False, is_flag=True)
@click.pass_context
def cli(ctx, main_param_bool, main_param_str, main_param_int):
    ctx.ensure_object(dict)
    ctx.obj['MAIN_PARAM_BOOL'] = main_param_bool
    ctx.obj['MAIN_PARAM_STR'] = main_param_str
    ctx.obj['MAIN_PARAM_INT'] = main_param_int


@cli.command()
@click.pass_context
@click.option("--vision_result", type=str)
@click.option("--hocr", type=str)
def convert(ctx, vision_result, hocr):
    click.echo('start convert')
    click.echo(ctx.obj['MAIN_PARAM_BOOL'])
    click.echo(ctx.obj['MAIN_PARAM_STR'])
    click.echo(ctx.obj['MAIN_PARAM_INT'])
    click.echo(vision_result)
    click.echo(hocr)


if __name__ == '__main__':
    cli(obj={})
