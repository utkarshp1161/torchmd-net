import subprocess
from setuptools import setup, find_packages

try:
    version = (
        subprocess.check_output(["git", "describe", "--abbrev=0", "--tags"])
        .strip()
        .decode("utf-8")
    )
except:
    print("Failed to retrieve the current version, defaulting to 0")
    version = "0"

setup(
    name="torchmd-net",
    version=version,
    packages=find_packages(),
    entry_points={"console_scripts": ["torchmd-train-rmd17 = torchmdnet.scripts.train_bebam_rmd17:main", "torchmd-train-lips = torchmdnet.scripts.train_bebam_lips:main", "torchmd-train-ala = torchmdnet.scripts.train_bebam_ala:main", "torchmd-train-3bpa = torchmdnet.scripts.train_bebam_3BPA:main", "torchmd-train-acac = torchmdnet.scripts.train_bebam_acac:main"]},
)
