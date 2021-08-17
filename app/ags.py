"""Functions to handle the AGS parser."""
import logging
from pathlib import Path
from textwrap import dedent
import subprocess

logger = logging.getLogger(__name__)

LOGFILE_TEMPLATE = dedent("""
    File Name: \t {filename}

    {error_message}
    """.strip())


def validate(filename: Path, results_dir: Path) -> Path:
    """Validate filename and write output to file in results_dir."""
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
        error = result.stderr
    if result.stdout.startswith('ERROR'):
        error = result.stdout

    if error:
        contents = LOGFILE_TEMPLATE.format(filename=filename.name, error_message=error)
        logfile.write_text(contents)

    return logfile


def convert(filename, results_dir):
    # Call ags4_cli to convert file
    pass


class Ags4CliError(Exception):
    """Class for exceptions resulting from ags4_cli call."""
    pass
