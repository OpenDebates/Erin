from cookiecutter.main import cookiecutter

from erin.cli import CommandFactory


class ScaffoldCommand(CommandFactory):
    def __init__(self, parser, *args, **kwargs):
        self.parser = parser.add_parser(*args, **kwargs)
        self.parser.set_defaults(action=self.run)

    def run(self, *sys_args, **kwargs):
        print("Enter the details for your project below!")
        extra_context = {
            "project_name": ("Project Name", "Bot"),
            "project_slug": ("Project Slug", "bot"),
            "version": ("Version Number", "0.0.0.dev0"),
            "config_file": ("Configuration File Name", "config.toml"),
            "_copy_without_render": ["plugins/*"],
        }
        for key, val in extra_context.items():
            if isinstance(val, tuple):
                setting = input(f"{val[0]} [{val[1]}]: ")
                if len(setting.strip()) == 0:
                    extra_context[key] = val[1]
                else:
                    extra_context[key] = setting

        cookiecutter(
            "https://github.com/OpenDebates/cookiecutter-erin.git",
            no_input=True,
            extra_context=extra_context,
        )
