#!/usr/bin/env python3
"""Build and run the official startup examples through the WSL sandbox."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def run(argv, cwd=ROOT, input_text=None):
    print("+ " + " ".join(map(str, argv)), flush=True)
    result = subprocess.run(list(map(str, argv)), cwd=cwd, input=input_text,
                            text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=600)
    print(result.stdout, end="", flush=True)
    if result.returncode:
        raise RuntimeError(f"Command returned {result.returncode}: {argv}")
    return result.stdout


def nemu():
    directory = ROOT / "nemu"
    if not (directory / ".config").exists():
        conf = directory / "tools/kconfig/build/conf"
        fixdep = directory / "tools/fixdep/build/fixdep"
        run(["make", "-C", directory, conf, fixdep])
        run([conf, "--alldefconfig", "Kconfig"], cwd=directory)
        run([conf, "--syncconfig", "Kconfig"], cwd=directory)
    run(["make", "-C", directory])
    output = run(["make", "-C", directory, "run"],
                 input_text="help\nc\nq\n")
    for expected in ("Welcome to", "help - Display information",
                     "HIT GOOD TRAP", "total guest instructions = 4"):
        if expected not in output:
            raise RuntimeError("Missing NEMU result: " + expected)
    print("NEMU_FIRST_RUN_PASS (official built-in image, 4 instructions)", flush=True)


def verilator():
    install = ROOT.parent / "tools/verilator-5.052"
    compiler = install / "bin/verilator"
    if not compiler.is_file():
        raise RuntimeError("Build the registered Verilator stable tool first")
    version = run([compiler, "--version"])
    if "Verilator 5.052" not in version:
        raise RuntimeError("Unexpected Verilator version")
    example = install / "share/verilator/examples/make_hello_c"
    work = ROOT.parent / "cache/first-run/verilator"
    shutil.copytree(example, work, dirs_exist_ok=True)
    run([compiler, "--cc", "--exe", "--build", "-j", "1", "-Wall",
         "top.v", "sim_main.cpp"], cwd=work)
    output = run([work / "obj_dir/Vtop"], cwd=work)
    if "Hello World!" not in output:
        raise RuntimeError("Missing official Verilator example result")
    print("VERILATOR_FIRST_RUN_PASS", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--component", choices=("all", "nemu", "verilator"), default="all")
    args = parser.parse_args()
    if Path(os.environ.get("NEMU_HOME", "")).resolve() != ROOT / "nemu":
        raise RuntimeError("Use the YSYX WSL sandbox entrypoint with Main as workbench")
    if os.getuid() == 0:
        raise RuntimeError("Do not build projects as root")
    if args.component in ("all", "nemu"):
        nemu()
    if args.component in ("all", "verilator"):
        verilator()


if __name__ == "__main__":
    main()
