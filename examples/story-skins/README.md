# Add Story skins for Jill or Barry

Story skins add selectable appearances in **PLEASE SELECT MAIN CAST** during
online or LAN Story Mode. Select Jill or Barry and use the up/down skin controls.
Their original appearances remain available.

## Build your package

1. Use this folder's `manifest.json` as the manifest at the root of your ZIP.
2. Choose a mod ID such as `yourname.story-skins`. Each skin's ID must start with
   that same ID followed by a dot. Give every skin a different ID.
3. Copy `skins/jill-custom.json` and/or `skins/barry-custom.json`. If you use only
   one, remove the unused path from `manifest.storySkins`.
4. Include your own model, preview, optional portrait and optional sounds at the
   paths you reference. The example assets themselves are not supplied.
5. Test the ZIP in SHATTERED. To submit it, follow [CONTRIBUTING](../../CONTRIBUTING.md).
   Copy the complete manifest beside `mod.zip`; both manifests must match.

For example, a ZIP with both sample definitions needs:

```text
YourStorySkins.zip
|-- manifest.json
|-- preview.png
|-- skins/
|   |-- jill-custom.json
|   `-- barry-custom.json
|-- models/
|   |-- jill-custom.pld
|   `-- barry-custom.pld
|-- portraits/
|   |-- jill-custom.png
|   `-- barry-custom.png
`-- voices/
    |-- barry-damage.wav
    |-- barry-death.wav
    `-- barry-dodge.wav
```

## Name and description in the selector

In a skin definition, `name` replaces the large character heading. It can display
your character's name instead of "Jill Valentine" or "Barry Burton". The optional
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
game's release number, so supporting updates do not require repackaging your mod.

## Models, portrait and sounds

- Set `target` to `Jill` or `Barry`. Use a supported player EMD or native PLD; the
  game handles supported model adaptation. Change the model path to match yours.
- A portrait is optional. Remove `portrait` to keep the target's normal portrait.
  Portraits and the package preview are noninterlaced, 8-bit PNGs, up to 2048x2048.
- The Jill example inherits all her action sounds. The Barry example supplies
  damage, death and dodge sounds, while inheriting missing banks. Use PCM WAVs.
- Optional voice banks are `damage`, `grabFront`, `grabRear`, `death` and `dodge`.
  Each bank accepts an array of files. Remove file references you do not supply.
- With `inheritMissing: true`, missing damage/grab/death banks use the target's
  sounds. With `false`, those missing banks are silent.
- Omit `dodge`, or use `[]`, to keep Jill's default dodge entry sound. Set
  `dodgeMode` to `Silent` to mute dodge entry sounds, including custom variants.
  `Default` keeps the usual behavior. There is no Story selection intro voice.

Skins keep their target's campaign behavior, animations and starting inventory.
Do not put `loadout`, `profile`, `animationBank` or `voices.intro` in a Story skin.

## Online and LAN

The selected model, portrait, name, description and sounds are shared with other
participants through the existing temporary skin download. **ALLOW OTHER USERS
CONTENT** controls those downloads. A participant who disables it must already
have the matching skin installed and enabled. Downloaded content is temporary;
it does not install or activate the whole mod on the other player's computer.

A single package can combine Story skins, Tyrant Battle characters, replacements
and backgrounds. Register each feature in its own manifest field. Only the Story
skin's resources and definition are shared when it is selected.
