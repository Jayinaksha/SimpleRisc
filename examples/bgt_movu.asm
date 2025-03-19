# Create a loop that increments a counter by a value loaded with movu.
# The loop uses CMP and BGT to decide when to exit.
            mov r1, 0      # Initialize loop counter r1 = 0.
            mov r2, 10     # Set loop limit r2 = 10.
loop_start: cmp r1, r2     # Compare counter (r1) with limit (r2).
            bgt end_loop   # If r1 > r2, branch to end_loop.
            movu r3, 5     # Use movu to load 5 (unsigned) into r3.
            add r1, r1, r3 # Increment r1 by r3.
            b loop_start   # Unconditionally jump back to loop_start.
end_loop:   movh r4, 2     # Use movh to load immediate 2 into the high half of r4.
                           # Expected: r4 becomes (2 << 16) = 131072.
            st r1, 200[r0] # Store final counter (r1) into memory at address (r0 + 200).
            ld r5, 200[r0] # Load the value from memory at address 200 into r5.

