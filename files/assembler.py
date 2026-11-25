"""Hack assembler (two-pass). Usage: python assembler.py File.asm
Extra feature (K = 32, K mod 3 = 2): warn if the same label is defined twice.
"""
import sys


class AsmError(Exception):
    pass


PREDEF = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
          'SCREEN': 16384, 'KBD': 24576}
PREDEF.update({f'R{i}': i for i in range(16)})

COMP_A = {'0': '101010', '1': '111111', '-1': '111010', 'D': '001100',
          'A': '110000', '!D': '001101', '!A': '110001', '-D': '001111',
          '-A': '110011', 'D+1': '011111', 'A+1': '110111', 'D-1': '001110',
          'A-1': '110010', 'D+A': '000010', 'D-A': '010011', 'A-D': '000111',
          'D&A': '000000', 'D|A': '010101'}
COMP = {c: '0' + b for c, b in COMP_A.items()}
for c, b in COMP_A.items():
    if 'A' in c:
        COMP[c.replace('A', 'M')] = '1' + b
# commutative forms the official assembler also accepts
for a, b in (('A+D', 'D+A'), ('A&D', 'D&A'), ('A|D', 'D|A'),
             ('M+D', 'D+M'), ('M&D', 'D&M'), ('M|D', 'D|M'),
             ('1+D', 'D+1'), ('1+A', 'A+1'), ('1+M', 'M+1')):
    if b in COMP:
        COMP[a] = COMP[b]

DEST = {'': '000', 'M': '001', 'D': '010', 'MD': '011', 'DM': '011',
        'A': '100', 'AM': '101', 'MA': '101', 'AD': '110', 'DA': '110',
        'AMD': '111'}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}


def clean(line):
    """Remove comments and all whitespace."""
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()


def assemble(lines):
    symbols = dict(PREDEF)
    labels_seen = set()
    prog, pc = [], 0

    # ---- First pass: drop comments/blank lines, record labels ----
    for n, raw in enumerate(lines, 1):
        s = clean(raw)
        if not s:
            continue
        if s.startswith('('):
            if not s.endswith(')') or len(s) < 3:
                raise AsmError(f'Line {n}: invalid label')
            label = s[1:-1]
            if label in labels_seen:  # extra feature (K mod 3 = 2)
                print(f'Warning: Line {n}: label ({label}) is defined more than once')
            labels_seen.add(label)
            symbols[label] = pc
        else:
            prog.append((n, s))
            pc += 1

    # ---- Second pass: translate to 16-bit binary ----
    out, next_var = [], 16
    for n, s in prog:
        if s.startswith('@'):
            sym = s[1:]
            if sym.isdigit():
                val = int(sym)
            else:
                if sym not in symbols:
                    symbols[sym] = next_var
                    next_var += 1
                val = symbols[sym]
            if val > 32767:
                raise AsmError(f'Line {n}: address too large')
            out.append(f'0{val:015b}')
        else:
            dest, rest = '', s
            if '=' in s:
                dest, rest = s.split('=', 1)
            comp, jump = rest, ''
            if ';' in rest:
                comp, jump = rest.split(';', 1)
            if dest not in DEST or comp not in COMP or jump not in JUMP:
                raise AsmError(f'Line {n}: invalid instruction')
            out.append('111' + COMP[comp] + DEST[dest] + JUMP[jump])
    return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python assembler.py File.asm')
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path) as f:
            binary = assemble(f.readlines())
    except AsmError as e:
        print(e)
        sys.exit(1)
    with open(path.rsplit('.', 1)[0] + '.hack', 'w') as f:
        f.write('\n'.join(binary) + '\n')
    print(f'Wrote {len(binary)} instructions')
