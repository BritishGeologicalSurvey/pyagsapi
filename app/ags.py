"""Functions to handle the AGS parser."""
import datetime as dt
import logging
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

RESPONSE_TEMPLATE = dedent("""
    File Name: \t {filename}
    File Size: \t {filesize:0.0f} kB
    Time (UTC): \t {time_utc}

    {message}
    """).strip()


def validate(filename: Path) -> str:
    """Validate filename and write output to file in results_dir."""
    logger.info("Validate called for %", filename.name)

    with TemporaryDirectory() as tmpdirname:
        logfile = Path(tmpdirname) / 'output.log'
        args = [
            'ags4_cli', 'check', filename, '-o', logfile
        ]
        # Use subprocess to run the file.  It will swallow errors.
        # If files have repeated headers the CLI will ask if they should be
        # renamed.  Passing input='n' answers 'n' to this question.
        # A timeout prevents the whole process hanging indefinitely.
        result = subprocess.run(args, capture_output=True,
                                input='n', text=True, timeout=30)
        logger.debug(result)
        log = logfile.read_text() if logfile.exists() else None

    # Generate response based on result of subprocess
    filesize = filename.stat().st_size / 1024
    time_utc = dt.datetime.now(tz=dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    if result.returncode != 0:
        use_template = True
        message = 'ERROR: ' + result.stderr
    elif result.stdout.startswith('ERROR: '):
        use_template = True
        message = result.stdout
    elif re.match(r'\d+ error\(s\) found in file', log):
        use_template = True
        # Files with lots of errors don't record metadata in their logs and
        # just list errors.  We can add filename back in via the template.
        message = log
    else:
        use_template = False

    if use_template:
        response = RESPONSE_TEMPLATE.format(filename=filename.name,
                                            filesize=filesize,
                                            time_utc=time_utc,
                                            message=message)
    else:
        response = log

    return response


def convert(filename: Path, results_dir: Path) -> Tuple[Optional[Path], str]:
    """
    Convert filename between .ags and .xlsx.  Write output to file in
    results_dir and return path alongside processing log."""
    new_extension = '.ags' if filename.suffix == '.xlsx' else '.xlsx'
    converted_file = results_dir / (filename.stem + new_extension)
    logger.info("Converting %s to %s", filename.name, converted_file.name)
    if not results_dir.exists():
        results_dir.mkdir()

    args = [
        'ags4_cli', 'convert', filename, converted_file
    ]
    # Use subprocess to run the file.  It will swallow errors.
    # A timeout prevents the whole process hanging indefinitely.
    result = subprocess.run(args, capture_output=True,
                            text=True, timeout=30)
    logger.debug(result)

    # Generate response based on result of subprocess
    filesize = filename.stat().st_size / 1024
    time_utc = dt.datetime.now(tz=dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    if result.returncode != 0:
        message = 'ERROR: ' + result.stderr
        converted_file = None
    elif result.stdout.startswith('ERROR: '):
        message = result.stdout
        converted_file = None
    else:
        message = f"SUCCESS: {filename.name} converted to {converted_file.name}"

    log = RESPONSE_TEMPLATE.format(filename=filename.name,
                                   filesize=filesize,
                                   time_utc=time_utc,
                                   message=message)

    return (converted_file, log)


def is_valid(filename: Path) -> bool:
    """
    Validate filename and parse returned log to determine if file is valid.
    """
    return log_is_valid(validate(filename))


def log_is_valid(log: str) -> bool:
    """
    Parse validation log to determine if file is valid.
    """
    return 'All checks passed!' in log


class Ags4CliError(Exception):
    """Class for exceptions resulting from ags4_cli call."""
    pass
