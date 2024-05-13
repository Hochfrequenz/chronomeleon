# Chronomeleon
🚧 Still Work In Progress!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python Versions (officially) supported](https://img.shields.io/pypi/pyversions/chronomeleon.svg)
![Pypi status badge](https://img.shields.io/pypi/v/chronomeleon)
![Unittests status badge](https://github.com/Hochfrequenz/chronomeleon/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/Hochfrequenz/chronomeleon/workflows/Coverage/badge.svg)
![Linting status badge](https://github.com/Hochfrequenz/chronomeleon/workflows/Linting/badge.svg)
![Black status badge](https://github.com/Hochfrequenz/chronomeleon/workflows/Formatting/badge.svg)

Chronomeleon is a Python package that converts and maps date and time information from their representation in one system to another.
It's meant to be used in data migration projects.

## Rationale
While converting a datetime alone is possible with either Python builtin tools or libraries like `pendulum` and `arrow`,
things become more complicated when you have to convert time slices or ranges or when the source and target system interpret dates and times differently.

Think your migrating e.g., contracts from system A to system B.
In system A might have an API, a data dump or something else from where you can read,
that a contract starts at `2024-01-01` and ends at `2024-06-30`.

Now assume, the same contract in system B starts at `2023-12-31T23:00:00Z` and ends at `2024-06-30T21:59:59Z`.

For this little conversion, although simple, you have to consider a lot:
* Are date and times implicitly "meant" in any certain time zone? Here, system A seems to implicitly assume, everything as German local time, whereas system B uses explicit UTC offsets.
* What about the resolution? Although using dates only might be sufficient for the modeling the business logic, as soon as the resolution of system B is higher, you have to start interpreting stuff.
  * What if there was a system C, which supported microseconds but only stored the date and time in a single integer?
* What about the end date (times)? It seems that system A uses the end date as inclusive (contract ends at the end of june), whereas system B uses it as exclusive (start of the followup contract == end of the previous contract).

Chronomeleon has two purposes:
1. It forces you to make assumptions explicit.
2. Once the assumptions are explicit, it helps you do the conversion.

The latter is no rocket science (and neither is any code in chronomeleon), but the former is crucial for a successful migration.

Chronomeleon makes your code more readable and makes your assumption clear.
This allows you to spot errors in your or your team mates code and explain, why things are done the way they are.

## How to use it?
Install it from pypi:
```bash
pip install chronomeleon
```

Then, in your code: Make assumptions about the source and target system explicit.
To do so, chronomeleon provides you with so-called ChronoConfig objects.
```python
```


## Setup for Local Development
Follow the instructions from our [template repository](https://github.com/Hochfrequenz/python_template_repository?tab=readme-ov-file#how-to-use-this-repository-on-your-machine).
tl;dr: `tox`.

## Contribute
You are very welcome to contribute to this template repository by opening a pull request against the main branch.
