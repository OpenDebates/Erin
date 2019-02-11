import re


def get_command_args(ctx, lower_case=True):
    """
    Gets the arguments passed to a command.

    :param ctx: pass a :class:`discord.ext.cli.Context` object
    :param lower_case: returns arguments in lower case
    :return: :obj:`list`
    """
    args = ctx.message.content.split(" ")
    if lower_case:
        args = [item.strip().lower() for item in args][1:]
    else:
        args = [item.strip() for item in args][1:]
    return args


def find_members(ctx):
    """
    Parses arguments passed to a command and returns a list of me

    :param ctx: pass a :class:`discord.ext.cli.Context` object
    :return: a list of :class:`discord.Member` objects
    """
    args = get_command_args(ctx)
    members = []
    for arg in args:
        arg = re.findall(r"\d{18}", arg)[0]
        if len(arg) == 18:
            member_obj = ctx.guild.get_member(int(arg))
            if member_obj:
                members.append(member_obj)
    members = list(set(members))
    return members
