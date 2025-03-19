# Set up two registers and compare them; use BGT to branch if the first is greater.
            mov r1, 50        # Set r1 = 50.
            mov r2, 40        # Set r2 = 40.
            cmp r1, r2        # Compare r1 with r2.
            bgt label_true    # Branch if r1 > r2 (i.e. if the carry flag is 0).
            mov r3, 0         # (This instruction should be skipped if branch is taken.)
            b label_end       # Unconditional branch to skip the following code.
label_true: mov r3, 1         # Set r3 = 1.
 label_end: st r3, 30[r0]     # Store r3 into memory at address (r0 + 30).
            ld r4, 30[r0]     # Load from memory at address 30 into r4.

