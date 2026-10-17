# Resident Evil: SHATTERED Mods

Community submissions for the mod browser built into **Resident Evil: SHATTERED**.

Players browse and download published mods from **MODS → BROWSE** in the game. Downloading does not activate a mod: restart the game, then enable it in **MODS**. Existing active mods and their priority are preserved.

Authors submit one folder per mod through a pull request. The folder contains the ZIP's complete manifest and either a small ZIP or a reference to a larger GitHub Release download. Maintainers review submissions; after merge, automation validates the exact package, publishes immutable Release assets, and updates the browser catalog. Authors do not edit a central catalog.

- [Submit or update a mod](CONTRIBUTING.md)
- [Examples](examples/README.md)
- [Report a problem](https://github.com/Depmify/Resident-Evil-SHATTERED-Mods/issues)

Published catalog: <https://depmify.github.io/Resident-Evil-SHATTERED-Mods/catalog.json>

This repository starts with no published mods. Templates and examples are outside `mods/` and never appear in the in-game browser.

## First pilot mod

Start with a small mod you have already tested in SHATTERED. Follow the [first submission instructions](CONTRIBUTING.md#first-submission), using a stable ID such as `yourname.pilot`. Include the finished ZIP and an identical copy of its complete manifest in `mods/yourname.pilot/`.

The pull request receives automatic validation. After approval and merge, the mod is published to the in-game browser automatically. An open or unapproved pull request does not publish a mod.
