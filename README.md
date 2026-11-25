https://marvelous-torrone-edabf7.netlify.app

# Capstone: Make the Computer Draw a Box

Course: Nand to Tetris – I (ETCNTC301), School of Engineering & Technology, K.R. Mangalam University

- **Name:** Chhavi Goyal
- **Roll number:** 2501730332
- **K:** 32

## What this project does

A Hack computer built in HDL, a two-pass assembler written in Python, and a Hack assembly program that draws a black box on the screen while any key is pressed and erases it when the key is released.

## My values (K = 32)

| Item | Value |
|---|---|
| Box start row | 32 |
| Start address | 16384 + 32 × 32 = 17408 |
| Box height | 20 rows (rows 32 to 51) |
| Box width | 16 × ((32 mod 4) + 1) = 16 pixels (1 word per row) |
| Extra assembler feature | K mod 3 = 2: warning when a label is defined twice |

## Files

| File | Purpose |
|---|---|
| `CPU.hdl` | Hack CPU (A and D registers, ALU, jump logic, PC) |
| `Memory.hdl` | RAM 16K, Screen, Keyboard in one address space |
| `Computer.hdl` | ROM32K + CPU + Memory |
| `assembler.py` | Two-pass Hack assembler (.asm to .hack) |
| `Box.asm` | Box program in Hack assembly |
| `Box.hack` | Box program assembled with my own assembler |
| `dup.asm` | Test file that defines a label twice (shows the warning) |
| `Capstone_Report.docx` | Project report |

## How to run

**Assembler** (needs Python 3):

```
python assembler.py Box.asm
```

This writes `Box.hack` in the same folder. To see the extra feature:

```
python assembler.py dup.asm
```

Expected output: `Warning: Line 5: label (LOOP) is defined more than once`

**HDL chips:** open the nand2tetris Hardware Simulator (web IDE), load `CPU.hdl`, `Memory.hdl` and `Computer.hdl`, and run the official `CPU.tst`, `Memory.tst` and `Computer.tst`.

**Box program:** load `Box.hack` (not `Box.asm`, so my own assembler's output is used), enable the keyboard, set animation to "no animation", run, and hold any key. The box appears while the key is held and disappears on release.

## How the assembler works

1. **First pass:** remove comments and blank lines, and record each label like `(LOOP)` with the address of the next real instruction. Labels take no space in the program.
2. **Second pass:** translate each instruction to 16 bits. New variables get RAM addresses starting at 16.

The extra feature (duplicate label warning) is in the first pass. Bad lines print `Line N: invalid instruction` instead of crashing.

## How Box.asm works

It loops forever: read the keyboard, set `color` to -1 (black) if a key is down or 0 (white) if not, then write that value into 20 rows of 1 word each starting at address 17408, moving 32 words down for each row.

Labels: LOOP = 0, DRAW = 8, PAINT = 10, ROWLOOP = 18, COLLOOP = 26.
Variables: color = 16, addr = 17, rows = 18, cols = 19, p = 20.
Total: 49 instructions.

## Changing the box (for quick edits)

- Move the box down by n rows: change `@17408` to `@(17408 + 32n)` as a number.
- Make the box wider: change `@1` in ROWLOOP to the number of 16-pixel words wanted.
- Change the height: change `@20` before ROWLOOP.
