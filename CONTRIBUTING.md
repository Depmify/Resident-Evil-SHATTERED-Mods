# Submit a SHATTERED mod

You can submit using GitHub's website. No packaging utility or local validator is required: keep your normal SHATTERED ZIP and its `manifest.json`.

## First submission

1. Fork this repository and create `mods/<mod-id>/`, using the exact lowercase `id` in your manifest. For example: `mods/yourname.survivor/`.
2. Copy the **complete** `manifest.json` from the root of your ZIP into that folder. Every field must match the ZIP's manifest, including characters, story skins, overrides, dependencies, preview path, and version.
3. Choose one package option below.
4. Open a pull request. Describe what the mod changes, its supported modes, its source, and any required mods.
5. Wait for validation and maintainer review. Fix reported issues in the same pull request.

For a ZIP up to **20 MiB**, upload it as `mod.zip`:

```text
mods/yourname.survivor/
├── manifest.json
└── mod.zip
```

For a larger ZIP, attach it to a public **GitHub Release** in your own repository. Add `package.json` instead of `mod.zip`:

```json
{
  "url": "https://github.com/yourname/your-mod/releases/download/v1.0.0/YourMod.zip",
  "sha256": "replace-with-the-64-character-lowercase-sha256-of-the-zip",
  "size": 123456789
}
```

`size` is the ZIP's exact size in bytes. The URL must download a ZIP directly from a public GitHub Release. Login pages, temporary download services, local addresses, and URLs containing credentials are rejected. Keep the source asset available while your submission is reviewed and published.

On Windows, you can obtain the values without installing anything:

```powershell
(Get-FileHash -LiteralPath .\YourMod.zip -Algorithm SHA256).Hash.ToLowerInvariant()
(Get-Item -LiteralPath .\YourMod.zip).Length
```

Each package must be **smaller than 2 GiB**, the GitHub Releases asset limit. This applies to both submission options. Submit the finished ZIP; avoid Git LFS pointers and additional source archives.

## Manifest and image

Use the existing SHATTERED manifest format. Provide a meaningful name, author, description, version, categories, and a PNG preview referenced by the manifest and included in the ZIP. The preview must be noninterlaced, 8-bit PNG, no larger than **2048 × 2048** or **4 MiB**. A landscape image is recommended.

`gameVersion` identifies the author's reference build and does not require an exact match. A compatible mod made for 0.1.6 does not need a new ZIP or version just because SHATTERED updates to 0.1.7 or later. Existing format 1 and 2 packages remain supported. Optional `compatibility.requires` entries identify specific feature contracts, such as `{ "capability": "story-skins", "version": 1 }`; most mods can omit them because the game derives requirements from their content. Missing capabilities, unsupported formats, invalid resources, and dependency problems still report concrete errors.

The mod ID must match its folder, begin with a lowercase letter or number, and use only lowercase letters, numbers, periods, underscores, and hyphens, up to 128 characters. Versions use numeric dot notation, such as `1.0.0` or `1.2.1`. Declare required mods by their IDs in `dependencies`; those mods must also be submitted to this catalog. Missing dependencies and cycles are rejected.

Keep executable files out of the ZIP. Publish only content you are permitted to distribute, and identify your source and credits in the description or an accompanying `README.md`. Structural validation checks packaging and metadata; it does not replace testing your mod in SHATTERED.

## Updating a mod

Edit the same `mods/<mod-id>/` folder. Increase the version, replace the ZIP or package reference, and copy the updated full manifest from the new ZIP. Open a new pull request.

Published versions are immutable. Changing a model, sound, preview, description, manifest, or any other ZIP content requires a higher version. Do not replace a previously published Release asset. Download URLs in the catalog always point to the exact bytes approved and mirrored by this repository, not to your external source URL.

## What automation handles

The publisher derives the browser's features and supported modes from the package's contents. A single ZIP can combine replacements, story skins, Tyrant Battle characters, and HD backgrounds. You do not need to split it into multiple submissions.

After approval and merge, automation publishes the ZIP to this repository's Releases and extracts its preview for GitHub Pages. The catalog changes only after every required Release asset is present and verified. You do not need to edit `catalog.json`, upload a second preview, or create an official Release yourself.
