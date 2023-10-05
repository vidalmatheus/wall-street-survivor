import inspect
from functools import wraps

from invoke import task


def projtask(func):
    """
    Task para ser executada na raiz do projeto.
    """

    @wraps(func)
    def wrapper(c, *args, **kwargs):
        with c.cd(c.config._project_prefix):
            return func(c, *args, **kwargs)

    wrapper.__signature__ = inspect.signature(func)
    return task(wrapper)


def _pipcompile(c, *, upgrade=None):
    upgrades = ""
    if upgrade:
        if upgrade == "ALL":
            upgrades = " --upgrade"
        else:
            for package in upgrade.split():
                upgrades += f' --upgrade-package "{package}"'

    output_file = "requirements.txt"
    input_files = "requirements.in"
    cmd = f"pip-compile --generate-hashes --allow-unsafe {upgrades} -o {output_file} {input_files}"
    print(cmd)
    c.run(cmd)


@projtask
def requirements(c, upgrade=None):
    _pipcompile(c, upgrade=upgrade)


@projtask
def lint(c):
    c.run("isort --profile black --line-length 120 --check .")
    c.run("black --line-length 120 --check .")


@projtask
def format(c):
    c.run("isort --profile black --line-length 120 .")
    c.run("black --line-length 120 .")
