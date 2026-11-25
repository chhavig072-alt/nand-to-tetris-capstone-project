// Box.asm  -  K = 32
// Box starts at row 32, is 20 rows tall, 16 pixels wide (1 word) at the left edge.
// Start address = SCREEN + 32*32 = 16384 + 1024 = 17408

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JNE          // key pressed -> draw
    @color
    M=0            // no key -> white (erase)
    @PAINT
    0;JMP
(DRAW)
    @color
    M=-1           // black
(PAINT)
    @17408
    D=A
    @addr
    M=D            // addr = start of row 32
    @20
    D=A
    @rows
    M=D            // rows = 20
(ROWLOOP)
    @1             // W = (32 mod 4) + 1 = 1 word per row
    D=A
    @cols
    M=D
    @addr
    D=M
    @p
    M=D            // p = start of this row
(COLLOOP)
    @color
    D=M
    @p
    A=M
    M=D            // paint one word (16 pixels)
    @p
    M=M+1
    @cols
    M=M-1
    D=M
    @COLLOOP
    D;JGT
    @32
    D=A
    @addr
    M=M+D          // next screen row (+32 words)
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @LOOP
    0;JMP
