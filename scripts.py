import subprocess
import sys


def format():
    subprocess.run([sys.executable, "-m", "black", "."])


if __name__ == "__main__":
    format()
