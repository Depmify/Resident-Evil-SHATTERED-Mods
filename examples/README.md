# Submission examples

Examples are templates, not published mods. Supply your own tested model, sounds, backgrounds, and preview inside your finished ZIP; no base-game resources are bundled here.

## A local model replacement

Use `replacement/manifest.json` as the ZIP's root manifest. Add your replacement at `models/player.emd` and your PNG preview at `preview.png`. The example replaces Chris; change the target to the supported player resource you intend to replace.

Create `mods/yourname.player-replacement/` in your fork, copy the complete manifest beside the finished `mod.zip`, and submit the folder. Other players do not need this cosmetic replacement to play online with you.

## A Tyrant Battle character

Use `tyrant-character/manifest.json` and `tyrant-character/characters/survivor.json`. Include the model, preview, portrait, and listed WAV files at their referenced paths inside the ZIP. The character definition controls its behavior profile, animation bank, loadout, and action voices.

For RE2/RE3 player models, reference the native `.pld` in `model`. SHATTERED performs the supported adaptation; do not preconvert it merely to submit a mod. Use a tested 15-part compatible player model.

## Story skins for Jill, Barry, Chris and Rebecca

Follow the [Story skin tutorial](story-skins/README.md). It includes a complete
manifest and separate [Jill](story-skins/skins/jill-custom.json),
[Barry](story-skins/skins/barry-custom.json), [Chris](story-skins/skins/chris-custom.json)
and [Rebecca](story-skins/skins/rebecca-custom.json) definitions, including custom selector
names and descriptions, models, portraits, action sounds and silent dodge audio.
Skins remain cosmetic and keep their target's campaign inventory and animations.
The Chris and Rebecca examples show numbered sound alternatives (1, 2) in the
voice arrays. List every file explicitly; numbered filenames are not discovered
automatically. The tutorial explains how to switch these skins in the selector.

## HD backgrounds

Use `hd-backgrounds/manifest.json` with the supported `hires/bgd` and `hires/mask` content in your ZIP. Keep original image identities and matching masks. Supply a PNG presentation image at `preview.png`.

HD packs often use the larger-package submission option. `templates/package.json` illustrates the source reference: replace its URL, hash, and size with values from your actual Release ZIP. The official catalog will mirror the approved package into its own Releases before advertising it.

## Combined packages

Combine `overrides`, `characters`, `storySkins`, and `roomVisuals` in one manifest when your mod needs several features. Copy that entire manifest to the submission folder. The publisher derives all feature labels; there is no separate catalog entry or manual list for each component.
