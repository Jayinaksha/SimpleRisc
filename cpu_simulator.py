class SimpleRiscCPU:
    def __init__(self):
        """Initialize CPU registers, memory, and program counter."""
        self.registers = [0] * 16 # 16 general- purpose registers (r0-r15)
        self.memory = [0] * 256 #Memory (256 words)
        self.PC = 0
        self.stack = []
        self.flags = {"Z": 0, "C":0} #Zero and carry flags are set zero
        self.instructions = [] # Store loaded instructions

    def load_progarm(self, hex_code):
        """Loads a list of hex instructions into memory."""
        binary_code = [bin(int(line,16))[2:].zfill(32) for line in hex_code.split("\n")]
        self.instructions = binary_code #Store the progarm instructions
        print("Progarm loaded into Memory!\n")

    def execute_instruction(self):
        """Fetches, decodes, and executes a single instruction."""
        if self.PC >= len(self.instructions): #Stop execution if PC exceeds progarm size
            return False
        instruction = self.instructions[self.PC] #Fetch instruction
        opcode = instruction[:5] #First 5 bits = opcode
        I = instruction[5] # 6th bit = immediate flag
        print(f"Executing: {instruction} (PC={self.PC})")

        if opcode == "00000": #ADD
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = self.registers[rs1] + self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = self.registers[rs1] + imm
            
        elif opcode == "00001": #SUB
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = self.registers[rs1] - self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = self.registers[rs1] - imm

        elif opcode == "00010": #mul
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = self.registers[rs1] * self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = self.registers[rs1] * imm

        elif opcode == "00011": #div
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = self.registers[rs1] / self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = self.registers[rs1] / imm

        elif opcode == "00100": #mod
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = self.registers[rs1] % self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = self.registers[rs1] % imm

        elif opcode == "00101": #cmp
            rs1 = int(instruction[6:10], 2)
            if I == "0":
                rs2 = int(instruction[10:14], 2)
                if self.registers[rs1] == self.registers[rs2]:
                    self.flags["Z"] = 1
                else:
                    self.flags["Z"] = 0
                if self.registers[rs1] < self.registers[rs2]:
                    self.flags["C"] = 1
                else:
                    self.flags["C"] = 0
            else:
                imm = int(instruction[12:28], 2)
                if self.registers[rs1] == imm:
                    self.flags["Z"] = 1
                else:
                    self.flags["Z"] = 0
                if self.registers[rs1] < imm:
                    self.flags["C"] = 1
                else:
                    self.flags["C"] = 0
        
        elif opcode == "00110": #and
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = self.registers[rs1] and self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = self.registers[rs1] and imm

        elif opcode == "00111": #or
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = self.registers[rs1] or self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = self.registers[rs1] or imm

        elif opcode == "01000": #not
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            self.registers[rd] = ~self.registers[rs1] and 0xFFFFFFFF

        elif opcode == "01001": #mov
            rd = int(instruction[6:10], 2)
            if I =="0":
                rs1 = int(instruction[10:14], 2)
                self.registers[rd] = self.registers[rs1]
            else:
                imm = int(instruction[12:28], 2)
                modifier = instruction[10:12]
                if modifier == "00":
                    self.registers[rd] = imm
                elif modifier == "01":
                    self.registers[rd] = imm
                elif modifier == "10":
                    self.registers[rd] = (imm << 16) | (self.registers[rd] & 0xFFFF) 

        
        elif opcode == "01010": #lsl
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = (self.registers[rs1] << self.registers[rs2]) & 0xFFFFFFFF
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = (self.registers[rs1]  << imm) & 0xFFFFFFFF

        elif opcode == "01011": #lsr
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                self.registers[rd] = (self.registers[rs1] >> self.registers[rs2]) & 0xFFFFFFFF
            else:
                imm = int(instruction[14:], 2)
                self.registers[rd] = (self.registers[rs1] >> imm) & 0xFFFFFFFF

        elif opcode == "01100": #asr
            rd = int(instruction[6:10], 2)
            rs1 = int(instruction[10:14], 2)
            if I == "0":
                rs2 = int(instruction[14:18], 2)
                if(self.registers[rs1] & (1 << 31)):
                   self.registers[rd] = (self.registers[rs1] >> self.registers[rs2]) | (0xFFFFFFFF << (32 - self.registers[rs2]))
                else:
                    self.registers[rd] = self.registers[rs1] >> self.registers[rs2]
            else:
                imm = int(instruction[14:], 2)
                if(self.registers[rs1] & (1 << 31)):
                   self.registers[rd] = (self.registers[rs1] >> imm) | (0xFFFFFFFF << (32 - imm))
                else:
                    self.registers[rd] = self.registers[rs1] >> imm

        elif opcode == "01101": #nop
            pass # Do nothing

        elif opcode == "01110": # ld
            rd = int(instruction[6:10], 2)
            base = int(instruction[10:14], 2)
            imm = int(instruction[14:], 2)
            mem_addr = self.registers[base] + imm
            if 0 <= mem_addr < len(self.memory):
                self.registers[rd] = self.memory[mem_addr]

        elif opcode == "01111": # st
            rd = int(instruction[6:10], 2)
            base = int(instruction[10:14], 2)
            imm = int(instruction[14:], 2)
            mem_addr = self.registers[base] + imm
            if 0 <= mem_addr < len(self.memory):
                self.memory[mem_addr] = self.registers[rd]

        elif opcode == "10000": #beq
            offset = int(instruction[5:], 2)
            if self.flags["Z"] == 1:
                self.PC = offset
                return True
        
        elif opcode == "10001": #bgt
            offset = int(instruction[5:], 2)
            if self.flags["C"] == 0:
                self.PC = offset
                return True
            
        elif opcode == "10010": #b
            offset = int(instruction[5:], 2)
            self.PC = offset
            return True
        
        elif opcode == "10011": #call
            offset = int(instruction[5:], 2)
            self.stack.append(self.PC+1)
            self.PC = offset
            return True
        
        elif opcode == "10100": #ret
            if self.stack:
                self.PC = self.stack.pop()
                return True
            return False
        else:
            print("Opcode invalid!")
            return None
        self.PC += 1
        return True
    
    def get_registers(self):
        """Returns the current state of registers as a string."""
        return "\n".join([f"r{i}: {self.registers[i]}" for i in range(16)])
    
    def get_memory(self):
        """Returns the current state of memory as a string."""
        return "\n".join([f"{i}: {self.memory[i]}" for i in range(len(self.memory)) if self.memory[i] !=0])

    def run (self):
        """Executes the loaded progarm step-by-step."""
        print("Starting Execution...\n")
        while self.execute_instruction():
            print(f"PC: {self.PC}, Registers: {self.registers}")
        print("\nExecution Halted.")
