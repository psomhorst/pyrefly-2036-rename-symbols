import warnings


class _RunIdentifier:
    value: int | None

    def __init__(self, value: int | None = None):
        self.value = value


_run_identifier = _RunIdentifier()


def get_run_identifier() -> int:
    """Update the run identifier and return it."""

    if _run_identifier.value is not None:
        return _run_identifier.value

    from project_settings import settings

    # Read the last run identifier
    last_run_identifier_path = settings.paths.run_identifier
    if last_run_identifier_path.exists():
        with last_run_identifier_path.open("r") as fh:
            last_run_identifier_str = fh.read().strip()
            try:
                last_run_identifier = int(last_run_identifier_str)
            except ValueError:
                warnings.warn(
                    f"Could not parse last run identifier '{last_run_identifier_str}'. "
                    "Starting from 0.",
                    RuntimeWarning,
                )
                last_run_identifier = 0
    else:
        last_run_identifier = 0

    # Increment the run identifier
    _run_identifier.value = last_run_identifier + 1

    # Write the new run identifier back to the file

    with last_run_identifier_path.open("w") as fh:
        fh.write(str(_run_identifier.value))

    str_identifier = settings.run_identifier.format.format(_run_identifier.value)
    increased_str_identifier = settings.run_identifier.format.format(
        int(_run_identifier.value * 1.1)
    )
    if len(increased_str_identifier) > len(str_identifier):
        warnings.warn(
            (
                "The run identifier will soon run out and increase in (formatted) length. "
                "This might cause file name issues. Consider changing the format."
            ),
            RuntimeWarning,
        )
    return str_identifier
