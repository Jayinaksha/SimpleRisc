mov r1, 10      #Set r1 to 10
mov r2, 10      #Set r2 to 10
cmp r1, r2      #Compare r1 with r2 (sets Zero flag if equal)
beq jump          #Branch to address 50 if r1 == r2
mov r3, 20      #This instruction won't execute because of the branch
jump:add r1, r1, r2
sub r3, r2, r1
