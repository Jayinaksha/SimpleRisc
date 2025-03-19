            mov r1, 0       #Set r1 to 0 (loop counter)
            mov r2, 5       #Set r2 to 5 (loop limit)
loop_start: cmp r1, r2      #Compare r1 (counter) with r2 (limit)
            beq end_loop    #If r1 == r2, jump to end_loop
            add r1, r1, 1   #Increment r1 by 1
            b loop_start    #Jump back to the start of the loop
end_loop:   mov r3, r1      #After loop, set r3 to the final value of r1 (should be 5)

