import re


def get_command_args(ctx):
    args = ctx.message.content.split(" ")
    args = [item.strip().lower() for item in args][1:]
    return args


def find_members(ctx):
    args = get_command_args(ctx)
    members = []
    for arg in args:
        arg = re.findall("\d{18}", arg)[0]
        if len(arg) == 18:
            member_obj = ctx.guild.get_member(int(arg))
            if member_obj:
                members.append(member_obj)
    members = list(set(members))
    return members
