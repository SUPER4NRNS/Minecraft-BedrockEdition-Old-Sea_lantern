# Minecraft Bedrock Sea Lantern Replacement Tool

A world conversion tool that replaces vanilla Sea Lantern blocks in already-generated chunks of Minecraft Bedrock Edition `.mcworld` files with the custom block `railfix:conductive_sea_lantern`.

The tool generates a **new world file without overwriting the original**.

**Important:** Back up your world and close Minecraft before running the converter. Always verify the converted world before using it as your primary save.

The corresponding behavior pack and resource pack must be installed and enabled separately. Without them, the custom blocks may not display or function correctly.

This project does not include any Minecraft world saves. For instructions on installing the required packs, please refer to the behavior pack installation guide.

## Usage (Windows)

Install **Python 3.12 (64-bit)**, then open a terminal in the project directory and run:

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 convert.py "C:\Path\OriginalWorld.mcworld" "C:\Path\ConvertedWorld.mcworld" --scan
py -3.12 convert.py "C:\Path\OriginalWorld.mcworld" "C:\Path\ConvertedWorld.mcworld"
```

The scan operation reads data from a temporary copy without modifying the original world.

During conversion, the tool extracts the world into a temporary directory, performs the replacement, and generates a new `.mcworld` file.

**The destination file must not already exist.**

Ensure that sufficient disk space is available for both the extracted world data and the resulting output file.

After importing the converted world, verify the following:

- Railway systems and powered rails
- Surrounding structures and buildings
- Redstone circuits and machinery
- Resource pack and behavior pack functionality

Keep the original world backup until the converted world has been thoroughly tested.

## Scope and Limitations

The converter processes already-generated chunks across all three dimensions:

- Overworld
- Nether
- The End

It supports chunk storage versions **1, 8, and 9**, and recognizes the following vanilla Sea Lantern identifiers:

- `minecraft:sea_lantern`
- `minecraft:seaLantern`
- `minecraft:sealantern`

Other chunk data is preserved during conversion.

### Unsupported Formats

If the converter detects the legacy numeric block ID `169`, it will terminate without generating an output file.

The conversion will also terminate if an unsupported relevant format or a parsing error is encountered.

### What the Converter Does Not Modify

The tool does not replace Sea Lantern references stored in:

- Containers or inventories
- Item data
- Structure files or saved structures
- Chunks generated after conversion

The converter matches specific block identifiers and is not guaranteed to support every Minecraft Bedrock Edition world format or future game versions.

**In-game verification is still required.**

### Testing and Compatibility

The underlying replacement method was previously tested on a Minecraft Bedrock Edition **1.26.63** world.

However, this independently packaged version still requires further validation in your own environment.

Compiled dependency versions may vary depending on the operating system and Python version.

The installation instructions above are intended for **Windows x64 with Python 3.12**.

---

## Known Issues and Usage Restrictions

### Design Philosophy

**This project follows the principle of minimal compatibility: it provides only the legacy behavior necessary to repair older worlds and does not encourage the continued use of outdated mechanics in newly created content.**

### 1. Compatibility with Vanilla Mechanics

The legacy-compatible Sea Lantern uses a custom block identifier and therefore cannot be guaranteed to behave identically to the original vanilla Sea Lantern in every situation.

**Known compatibility risk: Conduit structures and other Update Aquatic mechanics that rely on recognizing the vanilla Sea Lantern block may not function correctly after conversion.**

If your world makes extensive use of Conduits or other mechanics that depend on vanilla Sea Lantern identification, proceed with caution.

Always create a complete backup before performing a global conversion.

### 2. Survival Mode Acquisition Restrictions

Legacy-compatible Sea Lanterns **have no crafting recipe, do not generate naturally, and have no other intended acquisition methods**.

Players can obtain them only through the following methods:

- Directly obtaining the block in Creative Mode.
- Mining existing legacy-compatible Sea Lantern blocks.
- Using the included conversion tool to convert existing vanilla Sea Lantern blocks in a world save.

These restrictions are intentional design decisions, **not bugs**.

### 3. Project Purpose and Long-Term Recommendations

This project is primarily intended to repair older Minecraft Bedrock Edition worlds containing buildings, railway systems, and redstone contraptions that stopped functioning correctly after changes to the redstone conductivity of Sea Lanterns.

**The project is not intended to restore legacy Sea Lanterns as a regularly obtainable building material in Survival Mode.**

We do not encourage players to use legacy-compatible Sea Lanterns when constructing new buildings or redstone contraptions.

Whenever practical, players are encouraged to gradually replace legacy-compatible blocks with vanilla Sea Lanterns and modern redstone designs after completing the world repair process.

**Legacy-compatible Sea Lanterns should be treated as a historical compatibility measure, not as a permanent replacement for vanilla Sea Lanterns.**

### 4. World Data and Add-on Dependencies

Global conversion modifies block data stored in the world save.

Removing the behavior pack **will not automatically restore converted blocks to their original vanilla identifiers**.

Converted legacy-compatible Sea Lanterns depend on the corresponding behavior pack to function correctly.

Do not remove the required behavior pack before completing a reverse conversion or otherwise restoring the affected blocks. Doing so may result in unknown blocks, missing content, or world compatibility issues.

**Always create a complete backup of your world before performing any bulk conversion operation.**
