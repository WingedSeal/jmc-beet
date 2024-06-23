import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from .config import VERSION


def get_beet_yaml(namespace: str, pack_format: str) -> str:
    return f"""output: build
require: [jmcbeet]

data_pack:
  load: [src]
  name: datapack
  pack_format: {pack_format}

pipeline: [mecha]

meta:
  mecha:
    formatting: minify
  jmc:
    namespace: {namespace}
    file: src/data/{namespace}/main.jmc
"""


def main():
    cwd = Path(os.getcwd())
    parser = argparse.ArgumentParser(description="JMC-Beet integration")
    parser.add_argument("--version", "-v", action="version", version=VERSION)
    subparser = parser.add_subparsers(dest="command", required=True)
    init_parser = subparser.add_parser(
        "init", help="initialize beet workspace for jmc")
    init_parser.add_argument("--namespace", "-n", required=False, type=str)
    init_parser.add_argument("--pack-format", "-pf", required=False, type=str)

    args = parser.parse_args()
    if args.command == "init":
        namespace = args.namespace
        if namespace is None:
            namespace = input("namespace: ")
        pack_format = args.pack_format
        if pack_format is None:
            pack_format = input("pack format: ")

    if not (cwd / "beet.yaml").is_file():
        with (cwd / "beet.yaml").open("w+") as file:
            file.write(get_beet_yaml(namespace, pack_format))

    namespace_folder = cwd / "src" / "data" / namespace
    namespace_folder.mkdir(parents=True, exist_ok=True)
    (namespace_folder / "main.jmc").touch()
    (namespace_folder / "main.hjmc").touch()

    retcode = subprocess.call(
        [sys.executable, "-m", "pip", "install", "mecha"])
    time.sleep(0.5)
    subprocess.call(["beet"])
    is_in_venv = sys.prefix != sys.base_prefix
    if retcode != 0:
        print(
            "\n[JMC-Beet] Unable to install `mecha`, administrator privileges required. Run `pip install mecha` manually."
        )
    if not is_in_venv:
        print("[JMC-Beet] Virtual environment not detected.")
