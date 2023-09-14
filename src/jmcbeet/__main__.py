import argparse
import os
from pathlib import Path
import subprocess
import sys

from .config import VERSION


def get_beet_yaml(namespace: str):
    return f"""output: build
require: [jmcbeet]

data_pack:
  load: [src]
  name: datapack

pipeline: [mecha]

meta:
  mecha:
    formatting: minify
  jmc:
    namespace: {namespace}
    file: src/data/{namespace}/jmc/main.jmc
"""


def main():
    cwd = Path(os.getcwd())
    parser = argparse.ArgumentParser(
        description="JMC-Beet integration")
    parser.add_argument("--version", "-v", action='version', version=VERSION)
    subparser = parser.add_subparsers(dest="command", required=True)
    init_parser = subparser.add_parser(
        "init", help="initialize beet workspace for jmc")
    init_parser.add_argument(
        "--namespace",
        "-n",
        required=False,
        type=str)

    args = parser.parse_args()
    if args.command == "init":
        namespace = args.namespace
        if namespace is not None:
            namespace = input("namespace: ")

    if not (cwd / "beet.yaml").is_file():
        with (cwd / "beet.yaml").open("wr") as file:
            file.write(get_beet_yaml(namespace))

    namespace_folder = cwd / "src" / "data" / namespace
    namespace_folder.mkdir(parents=True, exist_ok=True)
    (namespace_folder / "main.jmc").touch()
    (namespace_folder / "main.hjmc").touch()

    is_in_venv = sys.prefix != sys.base_prefix
    if not is_in_venv:
        window_activate = r"`venv\Scripts\activate`"
        unix_activate = r"`source venv\bin\activate`"
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        if os.name == "nt":
            subprocess.check_call([r"venv\Scripts\activate"])
        else:
            subprocess.check_call(["source", "venv/bin/activate"])

    subprocess.check_call([sys.executable, "-m", "pip", "install", "mecha"])
    subprocess.check_call(["beet"])
