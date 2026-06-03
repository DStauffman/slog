r"""
File that acts as a sole-source for version history.

Notes
-----
#.  Written by David C. Stauffer in February 2022.

"""

# %% Constants
version_info = (1, 5, 1)

# Below is data about the minor release history for potential use in deprecating older support.
# For inspiration, see: https://numpy.org/neps/nep-0029-deprecation_policy.html

data = """Feb 22, 2022: slog 0.9
Aug 10, 2022: slog 1.0
Oct 26, 2023: slog 1.1
Jun 24, 2024: slog 1.2
Feb 04, 2025: slog 1.3
Apr 16, 2025: slog 1.4
Jun 20, 2025: slog 1.5
"""

# Historical notes:
# v0.9 Initial release after splitting from the dstauffman library.
# v1.0 Official baseline release.
# v1.1 Updates to black v23, mypy v1.6, Python v3.12.
# v1.2 Use newer typing standards from Python v3.10+.
# v1.3 Support Python v3.13, drop explicit ClassVar decorations.
# v1.4 Ditch poetry entirely, use setuptools (and uv instead).
# v1.5 Added files.py for reading and writing files and folders.
