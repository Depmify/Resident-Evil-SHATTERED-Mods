# Add Story skins for Jill, Barry, Chris or Rebecca

Story skins add selectable appearances in **PLEASE SELECT MAIN CAST** during
online or LAN Story Mode. Select the target character and use the up/down skin controls.
Their original appearances remain available.

Chris and Rebecca use the second cast page and become selectable after Jill and
Barry are confirmed, following Story Mode's normal cast rules. Move left/right
to highlight Chris or Rebecca, then up/down to change that character's skin
before confirming. Use the selector's keyboard or controller skin controls. Adding a skin does
not unlock a role or replace the original appearance.

## Build your package

1. Use this folder's `manifest.json` as the manifest at the root of your ZIP.
2. Choose a mod ID such as `yourname.story-skins`. Each skin's ID must start with
   that same ID followed by a dot. Give every skin a different ID.
3. Copy the definitions you want: `skins/jill-custom.json`, `skins/barry-custom.json`,
   `skins/chris-custom.json` and/or `skins/rebecca-custom.json`. Remove unused paths
   from `manifest.storySkins`.
4. Include your own model, preview, optional portrait and optional sounds at the
   paths you reference. The example assets themselves are not supplied.
5. Test the ZIP in SHATTERED. To submit it, follow [CONTRIBUTING](../../CONTRIBUTING.md).
   Copy the complete manifest beside `mod.zip`; both manifests must match.

For example, a ZIP using the four sample definitions needs:

```text
YourStorySkins.zip
|-- manifest.json
|-- preview.png
|-- skins/
|   |-- jill-custom.json
|   |-- barry-custom.json
|   |-- chris-custom.json
|   `-- rebecca-custom.json
|-- models/
|   |-- jill-custom.pld
|   |-- barry-custom.pld
|   |-- chris-custom.pld
|   `-- rebecca-custom.pld
|-- portraits/
|   |-- jill-custom.png
|   |-- barry-custom.png
|   |-- chris-custom.png
|   `-- rebecca-custom.png
`-- voices/
    |-- barry-damage.wav
    |-- barry-death.wav
    |-- barry-dodge.wav
    |-- chris/
    |   |-- damage-1.wav
    |   |-- damage-2.wav
    |   |-- grab-front-1.wav
    |   |-- grab-front-2.wav
    |   |-- grab-rear-1.wav
    |   |-- grab-rear-2.wav
    |   |-- death-1.wav
    |   |-- death-2.wav
    |   |-- dodge-1.wav
    |   `-- dodge-2.wav
    `-- rebecca/
        |-- damage-1.wav
        |-- damage-2.wav
        |-- grab-front-1.wav
        |-- grab-front-2.wav
        |-- death-1.wav
        `-- death-2.wav
```

## Name and description in the selector

In a skin definition, `name` replaces the large character heading. It can display
your character's name instead of the target's original name. The optional
`description` replaces the text below that character. For example:

```json
{
  "id": "yourname.story-skins.elza",
  "name": "Elza Walker",
  "description": "A determined survivor. Ready to face the mansion's horrors.",
  "target": "Jill",
  "model": "models/elza.pld",
  "voices": { "inheritMissing": true }
}
```

Omit `description`, or leave it empty, to keep the target's normal description.
Keep names and descriptions short: long names are shortened to fit the heading;
descriptions wrap and are shortened with `...` if they exceed the panel. Names
accept up to 120 characters and descriptions up to 512. These are plain text,
without formatting markup. A `\n` in the JSON string starts a new line.

These fields belong to the **skin JSON**. The manifest's `name` and `description`
describe the whole package in the Mod Browser.

Keep `story-skin-selection-text` contract 1 in `compatibility.requires` when your
mod needs custom selector text. It identifies the feature independently of the
game’s release number, so supporting updates do not require repackaging your mod.

Keep `story-skins-extended-cast` contract 1 for any package containing Chris or
Rebecca skins. It lets older games report the missing feature instead of relying
on a game version match. If you remove both definitions and only target Jill or
Barry, you can remove this extra requirement too.

## Models, portrait and sounds

- Set `target` to `Jill`, `Barry`, `Chris` or `Rebecca`. Use a supported player EMD or native PLD; the
  game handles supported model adaptation. Change the model path to match yours.
- A portrait is optional. Remove `portrait` to keep the target's normal portrait.
  Portraits and the package preview are noninterlaced, 8-bit PNGs, up to 2048x2048.
- The Jill example inherits all her action sounds. The Barry example supplies
  damage, death and dodge sounds, while inheriting missing banks. Use PCM WAVs.
- The [Chris example](skins/chris-custom.json) supplies two variants for every
  reaction bank, including dodge. The [Rebecca example](skins/rebecca-custom.json)
  supplies two hurt, front-grab and death variants, inherits rear-grab sounds and
  deliberately mutes dodge entry audio. Change these choices to suit your skin.
- Optional voice banks are `damage`, `grabFront`, `grabRear`, `death` and `dodge`.
  Each bank accepts an array of files. Remove file references you do not supply.
- With `inheritMissing: true`, missing damage/grab/death banks use the target's
  sounds. With `false`, those missing banks are silent.
- Omit `dodge`, or use `[]`, to keep the normal dodge surface sound without an added voice. Set
  `dodgeMode` to `Silent` to mute dodge entry sounds, including custom variants.
  `Default` keeps the usual behavior. There is no Story selection intro voice.

Skins keep their target's campaign behavior, animations and starting inventory.
Do not put `loadout`, `profile`, `animationBank` or `voices.intro` in a Story skin.

## Gameplay and cutscene appearances

Your skin's single `model` entry applies to gameplay and **in-engine cutscenes**:
native scene variants, alternate outfits and the computer terminal's close-up
arms use the selected skin too. You do not need additional definitions or asset
overrides for every original EMD. SHATTERED keeps the scene's own animation bank,
timing and equipped weapon. In online/LAN sessions, the appearance belongs to the
selected cast role even when its player is in a different room.

For example, the Chris template uses `models/chris-custom.pld` for both his
playable model and his scene variants. The same rule applies to the Jill, Barry
and Rebecca templates. Terminal close-ups use that model's forearm and hand
geometry; a rigid hand remains rigid when the skin has no articulated fingers.
Existing skin ZIPs receive this behavior automatically after updating SHATTERED.
Prerendered FMV videos have their own recorded images and do not change with a model skin.

## Multiple sound alternatives: 1, 2, 3...

Put all alternatives inside the bank's array, using paths relative to the ZIP root:

```json
"voices": {
  "inheritMissing": true,
  "damage": ["voices/chris/damage-1.wav", "voices/chris/damage-2.wav"],
  "death": ["voices/chris/death-1.wav", "voices/chris/death-2.wav"],
  "dodge": ["voices/chris/dodge-1.wav", "voices/chris/dodge-2.wav"],
  "dodgeMode": "Default"
}
```

To add a third hurt sound, include `voices/chris/damage-3.wav` in the ZIP and add
its path as a third entry in `damage`. Each bank accepts up to **32 PCM WAV files**.
The numbers are just filenames; they are not special JSON keys. Do not create
`damage1`, `damage2`, `death1` or `dodge2` fields. Files are not discovered simply
because their names end in a number: every variant must be listed explicitly.

One variant plays per reaction. Selection uses the character's running voice
sequence across reaction banks, so it does not play the entire array at once or
maintain a separate 1, 2 cycle for each bank. These arrays work for all four Story
targets and for Tyrant Battle characters. Set `dodgeMode` to `Silent` to suppress
all dodge entry sounds even if the `dodge` array contains files.

## Online and LAN

The selected model, portrait, name, description and sounds are shared with other
participants through the existing temporary skin download. **ALLOW OTHER USERS
CONTENT** controls those downloads. A participant who disables it must already
have the matching skin installed and enabled. Downloaded content is temporary;
it does not install or activate the whole mod on the other player's computer.

A single package can combine Story skins, Tyrant Battle characters, replacements
and backgrounds. Register each feature in its own manifest field. Only the Story
skin's resources and definition are shared when it is selected.
