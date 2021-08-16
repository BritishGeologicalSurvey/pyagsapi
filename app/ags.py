"""Functions to handle the AGS parser."""
from pathlib import Path
import subprocess


def validate(filename, results_dir):
    logfile = Path(results_dir) / Path(filename).stem + '.log'
    args = [
        'ags4_cli', 'check', filename, '-o', logfile
    ]
    result = subprocess.run(args, check=True, capture_output=True)
    print(result)
    print(result.stdout.decode())


def convert(filename, results_dir):
    # Call ags4_cli to convert file
    pass


if __name__ == '__main__':
    validate('/home/jostev/gitlab/ags-python-library/tests/test_files/example1.ags')
