"""Functions to handle the AGS parser."""
import logging
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)


def validate(filename: Path, results_dir: Path) -> Path:
    """Validate filename and write output to file in results_dir."""
    if not results_dir.exists():
        results_dir.mkdir()
    logfile = results_dir / (filename.stem + '.log')

    args = [
        'ags4_cli', 'check', filename, '-o', logfile
    ]
    try:
        result = subprocess.run(args, check=True, capture_output=True)
        logger.debug(result)
    except subprocess.CalledProcessError as exc:
        logger.exception(exc)
        raise Ags4CliError(exc)

    if error_message := result.stdout.decode().startswith('ERROR'):
        raise Ags4CliError(error_message)

    return logfile


def convert(filename, results_dir):
    # Call ags4_cli to convert file
    pass


class Ags4CliError(Exception):
    """Class for exceptions resulting from ags4_cli call."""
    pass
