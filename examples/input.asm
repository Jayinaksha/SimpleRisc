mov r1, 10     #Set r1 to 10
call jump        # Call function at address 30
mov r2, 20      #This instruction won't execute immediately
jump:mov r3, 30     #This instruction will execute after jump from the function
ret                  # return the function
