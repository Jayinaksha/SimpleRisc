import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk, StringVar
from cpu_simulator import SimpleRiscCPU
opcodes = {
    "add": "00000",
    "sub": "00001",
    "mul": "00010",
    "div": "00011",
    "mod": "00100",
    "cmp": "00101",
    "and": "00110",
    "or" : "00111",
    "not": "01000",
    "mov": "01001",
    "lsl": "01010",
    "lsr": "01011",
    "asr": "01100",
    "nop": "01101",
    "ld" : "01110",
    "st" : "01111",
    "beq": "10000",
    "bgt": "10001",
    "b"  : "10010",
    "call":"10011",
    "ret": "10100",
    #Type modifiers
    "movu":"01001",
    "movh":"01001"
}

registers = {f"r{i}": f"{i:04b}" for i in range(16)}

#identify labels
symbol_table = {}
def first_pass(assembly_code):
    """Pass 1: Identifies labels and stored their memory addresses."""
    address = 0
    for line in assembly_code.split("\n"):
        line=line.split("#")[0].strip()
        if not line :
            continue
        if ":"in line:
            label = line.split(":")[0].strip()
            symbol_table[label]= address
            address += 1
        else:
            address += 1

# assemble_instruction
#input: assembly instructions as "add r1, r2, r3"
#output: binary as "00000000000100001" 32 bits
def assemble_instruction(instruction):
    if ":" in instruction:
        parts = instruction.split(":")[1].split()
    else:
        parts = instruction.split() #split instruction into parts for conversion
    if not parts:
        print("Invalid instruction")
        return None
    
    mnemonic = parts[0]
    
    #Handeling different instruction formats for different address types
    #case 0
    if mnemonic in ["nop", "ret"]:
        return f"{opcodes[mnemonic]}{'0'*27}"
    #case1
    elif mnemonic in ["beq", "bgt", "b", "call"]:
        label = parts[1]
        if label in symbol_table:
            offset = symbol_table[label]
        else:
            print(f"Undefined label {label}")
            return None
        offset_binary = f"{offset:027b}"
        return f"{opcodes[mnemonic]}{offset_binary}"
    #case2
    elif mnemonic in ["cmp", "not", "mov"]:
        rd = registers[parts[1].strip(",")]
        if parts[2].startswith("r"): #register format
            rs2 = registers[parts[2]]
            return f"{opcodes[mnemonic]}0{rd}{rs2}{'0'*18}"
        else:
            imm = int(parts[2])
            imm_binary = f"{imm & 0xFFFF:016b}" # only lower 16 bits
            modifier = "00" # default 
            return f"{opcodes[mnemonic]}1{rd}{modifier}{imm_binary}{'0'*4}"

    #case2a
    elif mnemonic in ["movu", "movh"]:
        rd = registers[parts[1].strip(",")]
        if parts[2].startswith("r"): #register format
            print("Invalid operand!")
            return None
        else:
            imm = int(parts[2])
            imm_binary = f"{imm & 0xFFFF:016b}" # only lower 16 bits
            if mnemonic in ["movu"]:
                modifier = "01"
            else:
                modifier = "10"
            return f"{opcodes[mnemonic]}1{rd}{modifier}{imm_binary}{'0'*4}"

    #case3
    elif mnemonic in ["add", "sub", "mul", "div", "mod", "and", "or", "lsl", "lsr", "asr"]:
        rd = registers[parts[1].strip(",")]
        rs1 = registers[parts[2].strip(",")]
        if parts[3].startswith("r"):
            rs2 = registers[parts[3]]
            return f"{opcodes[mnemonic]}0{rd}{rs1}{rs2}{'0'*14}"
        else:
            imm = int(parts[3])
            imm_binary = f"{imm:018b}"
            return f"{opcodes[mnemonic]}1{rd}{rs1}{imm_binary}"
    #case4
    elif mnemonic in ["ld", "st"]:
        rd = registers[parts[1].strip(",")]
        base_register = registers[parts[2].split("[")[1].strip("]")]
        imm = int(parts[2].split("[")[0])
        imm_binary = f"{imm:018b}"
        return f"{opcodes[mnemonic]}1{rd}{base_register}{imm_binary}"
    else:
        print(f"Unknown instruction {mnemonic}")
        return None

def assemble_progarm(assembly_code):
    first_pass(assembly_code)
    binary_output = []
    error_lines = []
    for i, line in enumerate(assembly_code.split("\n")):
        line = line.split("#")[0].strip()
        if  not line:
            continue
        binary_instruction = assemble_instruction(line)
        if binary_instruction is not None:
            binary_output.append(binary_instruction)
        else:
            error_lines.append(i+1)
            print(f"Warning: Invalid instruction {line}")
    return "\n".join(binary_output), error_lines

def binary_to_hex(binary_code):
    return hex(int(binary_code, 2))[2:].zfill(8)

##################################################################################
#"""CLI logic"""
# def main():
#     """Main function to take user input and assemble code."""
#     print("SimpleRisc Assembler")
#     mode = input("Enter '1' for manual input, '2' for file input: ")
#     if mode == "1":
#         print("Enter your assebmly code (type 'END' to finish):")
#         user_input = []
#         while True:
#             line = input()
#             if line.strip().upper()=="END":
#                 break
#             user_input.append(line)
#         assembly_code = "\n".join(user_input)
#     elif mode == "2":
#         file_path = input("Enter the assembly file path:")
#         try:
#             with open(file_path, "r") as f:
#                 assembly_code = f.read()
#         except FileNotFoundError:
#             print("Error: File not found.")
#             return
#     else:
#         print("Invalid option.\n Please choose a valid option")
#         return
#     first_pass(assembly_code)
#     binary_output = assemble_progarm(assembly_code)
#     hex_output = "\n".join(binary_to_hex(line) for line in binary_output.split("\n"))

#     print("\nAssembled Hex Code:")
#     print(hex_output)
#     save_file = input("Save output to file? (y/n):")
#     if save_file.lower() == "y":
#         output_file = input("Enter output file name (e.g., output.hex):")
#         with open(output_file, "w") as f:
#             f.write(hex_output)
#         print(f"Hex code saved to {output_file}")
# if __name__ == "__main__":
#     main()
# # assembly_code = """
# # add r1, r2, r3 #hi
# # sub r4, r5, 10 
# # beq 20 
# # ld r1, 4[r2] 
# # nop
# # """
# # binary_output = assemble_progarm(assembly_code)
# # hex_output = "\n".join(binary_to_hex(line) for line in binary_output.split("\n"))

# # print(hex_output)
########################################################################################################
class AssemblerGui:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleRisc Assembler")
        # --Menu Bar--
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open File", command=self.load_file)
        file_menu.add_command(label="Save Output", command=self.save_output_hex)
        self.menu.add_cascade(label="File", menu=file_menu)

        # -- Assemble Input Box--
        self.text_input = tk.Text(root, height=20, width=150)
        self.text_input.pack(pady=10)

        # --Assemble Button--
        self.assemble_button = tk.Button(root, text="Assemble", command=self.assemble_code)
        self.assemble_button.pack()
        # --DropDown selection
        self.format_var = StringVar(value="Hex")
        self.format_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.format_var,
            values=["Hex", "Binary"],
            width=8
        )
        self.format_dropdown.pack(side="right",padx=5)
        # --Output Box--
        self.output_label = tk.Label(root, text="Assembled Machine Code (Hex):")
        self.output_label.pack()

        self.output_text = tk.Text(root, height=10, width=150, bg="#f4f4f4")
        self.output_text.pack(pady=10)

        #-- Save to file button--
        self.save_button = tk.Button(root, text="Save output", command=self.save_file)
        self.save_button.pack()

        #-- Run CPU Button__
        self.run_button = tk.Button(root, text="Run CPU", command=self.run_cpu)
        self.run_button.pack()

        #--Registers Output Box--
        self.registers_label = tk.Label(root, text="CPU Registers:")
        self.registers_label.pack()
        self.registers_text = tk.Text(root, height=8, width=100, bg="#e8f4f8")
        self.registers_text.pack(pady=5)

        #--Memory Output Box --
        self.memory_label = tk.Label(root, text="Memory Content:")
        self.memory_label.pack()
        self.memory_text = tk.Text(root, height=8, width=100, bg="#f8e8e8")
        self.memory_text.pack(pady=5)

    def assemble_code(self):
        """ Coverts the assembly code to hex and displays it."""
        selected_format = self.format_var.get()
        assemble_code = self.text_input.get("1.0", tk.END).strip()
        if not assemble_code:
            messagebox.showwarning("warning", "no assembly code provided!")
            return
        binary_output, error_lines = assemble_progarm(assemble_code)
        hex_output = "\n".join(binary_to_hex(line) for line in binary_output.split("\n"))
        if selected_format == "Hex":
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, hex_output)
        else:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, binary_output)

        #--Handle/Highlite errors--
        self.text_input.tag_remove("error","1.0", tk.END)
        if error_lines:
            messagebox.showerror("Error", f"Syntax error in lines: {error_lines}")
            for line in error_lines:
                start = f"{line}.0"
                end = f"{line}.end"
                self.text_input.tag_add("error", start, end)
                self.text_input.tag_config("error", foreground="red")

    def save_file(self):
        selected_format = self.format_var.get()
        if selected_format == "Hex":
            self.save_output_hex()
        else:
            self.save_output_bin()

    def load_file(self):
        """Open a file dialog to load an assembly file into the text editor."""
        file_path = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as f:
                assemble_code = f.read()
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, assemble_code)

    def save_output_hex(self):
        """Saves the assembled hex output to a file."""
        hex_output = self.output_text.get("1.0", tk.END).strip()
        if not hex_output:
            messagebox.showwarning("Warning", "No output to save!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".hex",
                                                 filetypes=[("Hex Files", "*.hex"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(hex_output)
            messagebox.showinfo("Success", f"Output saved to {file_path}")

    def save_output_bin(self):
        """Saves the assembled hex output to a file."""
        bin_output = self.output_text.get("1.0", tk.END).strip()
        if not bin_output:
            messagebox.showwarning("Warning", "No output to save!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".bin",
                                                 filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(bin_output)
            messagebox.showinfo("Success", f"Output saved to {file_path}")
    
    def run_cpu(self):
        """Runs the assembled hex code in the CPU simulator."""
        selected_format = self.format_var.get()
        if selected_format == "Hex":
            hex_code = self.output_text.get("1.0", tk.END).strip()
            if not hex_code:
                messagebox.showwarning("Warning", "No hex code available to run!")
                return
        else:
            binary_output = self.output_text.get("1.0", tk.END).strip()
            hex_code = "\n".join(binary_to_hex(line) for line in binary_output.split("\n"))
        self.cpu = SimpleRiscCPU()
        self.cpu.load_progarm(hex_code)
        self.cpu.run()

        #Update Registers and Memory in GUI
        self.registers_text.delete("1.0", tk.END)
        self.registers_text.insert(tk.END, self.cpu.get_registers())

        self.memory_text.delete("1.0", tk.END)
        self.memory_text.insert(tk.END, self.cpu.get_memory())
#--Run GUI--
if __name__ == "__main__":
    root = tk.Tk()
    gui = AssemblerGui(root)
    root.mainloop()