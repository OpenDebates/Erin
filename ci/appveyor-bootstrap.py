"""
AppVeyor will at least have few Pythons around so there's no point of
implementing a bootstrapper in PowerShell.

This is a port of https://git.io/fhQA7
with various fixes and improvements that just weren't feasible
to implement in PowerShell.
"""
from os import environ
from os.path import exists
from subprocess import check_call

from urllib.request import urlretrieve

BASE_URL = "https://www.python.org/ftp/python/"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
GET_PIP_PATH = r"C:\get-pip.py"
URLS = {
    ("3.6", "64"): BASE_URL + "3.6.8/python-3.6.8-amd64.exe",
    ("3.6", "32"): BASE_URL + "3.6.8/python-3.6.8.exe",
    ("3.7", "64"): BASE_URL + "3.7.2/python-3.7.2-amd64.exe",
    ("3.7", "32"): BASE_URL + "3.7.2/python-3.7.2.exe",
}
INSTALL_CMD = {
    "3.6": [["{path}", "/quiet", "TargetDir={home}"]],
    "3.7": [["{path}", "/quiet", "TargetDir={home}"]],
}


def download_file(url, path):
    print(f"Downloading: {url} (into {path})")
    progress = [0, 0]

    def report(count, size, total):
        progress[0] = count * size
        if progress[0] - progress[1] > 1000000:
            progress[1] = progress[0]
            print("Downloaded {:,}/{:,} ...".format(progress[1], total))

    dest, _ = urlretrieve(url, path, reporthook=report)
    return dest


def install_python(version, arch, home):
    print(
        "Installing Python", version, "for", arch, "bit architecture to", home
    )
    if exists(home):
        return

    path = download_python(version, arch)
    print("Installing", path, "to", home)
    success = False
    for cmd in INSTALL_CMD[version]:
        cmd = [part.format(home=home, path=path) for part in cmd]
        print("Running:", " ".join(cmd))
        try:
            check_call(cmd)
        except Exception as exc:
            print("Failed command", cmd, "with:", exc)
            if exists("install.log"):
                with open("install.log") as fh:
                    print(fh.read())
        else:
            success = True
    if success:
        print("Installation complete!")
    else:
        print("Installation failed")


def download_python(version, arch):
    for _ in range(3):
        try:
            return download_file(URLS[version, arch], "installer.exe")
        except Exception as exc:
            print("Failed to download:", exc)
        print("Retrying ...")


def install_pip(home):
    pip_path = home + "/Scripts/pip.exe"
    python_path = home + "/python.exe"
    if exists(pip_path):
        print("pip already installed.")
    else:
        print("Installing pip...")
        download_file(GET_PIP_URL, GET_PIP_PATH)
        print("Executing:", python_path, GET_PIP_PATH)
        check_call([python_path, GET_PIP_PATH])


def install_packages(home, *packages):
    cmd = [home + "/Scripts/pip.exe", "install"]
    cmd.extend(packages)
    check_call(cmd)


if __name__ == "__main__":
    install_python(
        environ['PYTHON_VERSION'], environ['PYTHON_ARCH'],
        environ['PYTHON_HOME']
    )
    install_pip(environ['PYTHON_HOME'])
    install_packages(
        environ['PYTHON_HOME'], "setuptools>=40.6.2", "wheel", "tox",
        "codecov", "virtualenv>=16.4.0", ". [TESTS]"
    )
