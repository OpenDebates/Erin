def get_command_args(ctx):
    args = ctx.mesage.content.split(" ")
    args = [item.strip().lower() for item in args][1:]
    return args
