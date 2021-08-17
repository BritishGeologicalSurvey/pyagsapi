"""Functions to handle the AGS parser."""
import logging
from pathlib import Path
from textwrap import dedent
import subprocess

logger = logging.getLogger(__name__)

LOGFILE_TEMPLATE = dedent("""
    File Name: \t {filename}

    {message}
    """).strip()


def validate(filename: Path, results_dir: Path) -> Path:
    """Validate filename and write output to file in results_dir."""
    logger.info("Validate called for %", filename.name)
    if not results_dir.exists():
        results_dir.mkdir()
    logfile = results_dir / (filename.stem + '.log')

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

    # Look for errors in the results
    error = None
    if result.returncode != 0:
        error = 'ERROR: ' + result.stderr
    if result.stdout.startswith('ERROR'):
        error = result.stdout

    if error:
        contents = LOGFILE_TEMPLATE.format(filename=filename.name, message=error)
        logfile.write_text(contents)

    return logfile


def convert(filename, results_dir):
    """Validate filename and write output to file in results_dir."""
    # Call ags4_cli to convert file
    if not results_dir.exists():
        results_dir.mkdir()

    new_extension = '.ags' if filename.suffix == '.xlsx' else '.xlsx'
    converted_file = results_dir / (filename.stem + new_extension)
    logfile = results_dir / (filename.name + '.log')

    args = [
        'ags4_cli', 'convert', filename, converted_file
    ]
    # Use subprocess to run the file.  It will swallow errors.
    # If files have repeated headers the CLI will ask if they should be
    # renamed.  Passing input='n' answers 'n' to this question.
    # A timeout prevents the whole process hanging indefinitely.
    result = subprocess.run(args, capture_output=True,
                            input='n', text=True, timeout=30)
    logger.debug(result)

    # Prepare log file content
    if result.returncode != 0:
        message = 'ERROR: ' + result.stderr
        converted_file = None
    elif result.stdout.startswith('ERROR'):
        message = result.stdout
        converted_file = None
    else:
        message = f"SUCCESS: {filename.name} converted to {converted_file.name}"

    contents = LOGFILE_TEMPLATE.format(filename=filename.name, message=message)
    logfile.write_text(contents)

    return (converted_file, logfile)


class Ags4CliError(Exception):
    """Class for exceptions resulting from ags4_cli call."""
    pass
