import os
import streamlit as st
from cpu_simulator import SimpleRiscCPU
from assembler_logic import assemble_progarm, binary_to_hex
st.title("SimpleRisc Assembler & CPU Simulator")

st.header("Assembly Input Upolad / Examples")

uploaded_file = st.sidebar.file_uploader("Upload an Assembly File", type=["asm", "txt", "all"])

# Option1: Uploaded an assembly file.
if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    st.session_state["assembly_code"] = file_content
    st.sidebar.success("File loaded successfully!")

#Option2. Choose from examples 
if os.path.isdir("examples"):
    example_files = [f for f in os.listdir("examples") if os.path.isfile(os.path.join("examples", f))]
    if example_files:
        selected_example = st.sidebar.selectbox("Or select an example file", example_files)
        if st.sidebar.button("Load Example"):
            with open(os.path.join("examples", selected_example), "r") as f:
                example_code = f.read()
            st.session_state["assembly_code"] = example_code
            st.sidebar.success(f"Example {selected_example} loaded!")

#Main area: Assembly code text area
st.header("Assembly Code Input")
if "assembly_code" in st.session_state:
    assembly_code = st.session_state["assembly_code"]
else:
    assembly_code = ""
assembly_code = st.text_area("Entre Assembly Code:", key="assembly_code", height=300)
output_format = st.selectbox("Output Format", ["Hex", "Binary"])

if st.button("Assemble"):
    if not assembly_code.strip():
        st.error("Please enter some assembly code!")
    else:
        binary_output, errors = assemble_progarm(assembly_code)
        if errors:
            st.error(f"Syntax error in lines: {errors}")
        if output_format == "Hex":
            assembled_output = "\n".join(binary_to_hex(line) for line in binary_output.split("\n"))
        else:
            assembled_output = binary_output
        st.subheader("Assembled Machine Code:")
        st.text_area("", assembled_output, height=150)
        st.session_state["assembled_code"] = assembled_output


        # Download Button: Provide file download for assembled output
        if output_format == "Hex":
            download_filename = "output.hex"
            download_data = assembled_output
        elif output_format == "Binary":
            download_filename = "output.bin"
            download_data = assembled_output

        st.download_button(
            label="Download Assembled Code",
            data=download_data,
            file_name=download_filename,
            mime="text/plain"
        )
else:
    if not assembly_code.strip():
        st.warning("Please enter some assembly code!")
    else:
        binary_output, errors = assemble_progarm(assembly_code)
        if errors:
            st.error(f"Syntax error in lines: {errors}")
        if output_format == "Hex":
            assembled_output = "\n".join(binary_to_hex(line) for line in binary_output.split("\n"))
        else:
            assembled_output = binary_output
        st.subheader("Assembled Machine Code:")
        st.text_area("", assembled_output, height=150)
        st.session_state["assembled_code"] = assembled_output


        # Download Button: Provide file download for assembled output
        if output_format == "Hex":
            download_filename = "output.hex"
            download_data = assembled_output
        elif output_format == "Binary":
            download_filename = "output.bin"
            download_data = assembled_output

        st.download_button(
            label="Download Assembled Code",
            data=download_data,
            file_name=download_filename,
            mime="text/plain"
        )
        # --- CPU Simulation ---

st.header("CPU Simulator")
if output_format == "Hex":
    if "assembled_code" in st.session_state:
        hex_input = st.session_state.assembled_code
    else:
        hex_input = st.text_area("Entre hex code to run:", height=150)
elif output_format == "Binary":
    if "assembled_code" in st.session_state:
        bin_input = st.session_state.assembled_code
        hex_input = "\n".join(binary_to_hex(line) for line in bin_input.split("\n"))
    else:
        bin_input = st.text_area("Entre binary code to run:", height=150)
        hex_input = "\n".join(binary_to_hex(line) for line in bin_input.split("\n"))
else:
    if "assembled_code" in st.session_state:
        assembled = st.session_state["assembled_code"]
        hex_input = assembled.split("\n\n")[0].replace("Hex Output:\n", "")
    else:
        hex_input = st.text_area("Enter hex code to run:", height=150)
if st.button("Run CPU"):
    if not hex_input.strip():
        st.error("No hex code available to run!")
    else:
        cpu = SimpleRiscCPU()
        cpu.load_progarm(hex_input)
        cpu.run()
        st.subheader("Cpu Registers")
        st.text_area("Registers", cpu.get_registers(), height=150)
        st.subheader("memory Content")
        mem_content = cpu.get_memory()
        if mem_content:
            st.text_area("Memory", mem_content, height=150)
        else:
            st.text("Memory is empty.")

with st.sidebar.expander("Instructions"):
    st.markdown("""
    ## SimpleRisc Assembler Instructions

    **How to Use This App:**

    - **Assembly Code Input:**  
      Type or paste your assembly code into the main text area.  
      
    - **File Upload:**  
      Use the file uploader on the sidebar to load an assembly file (`.asm`, `.txt`, or any file).
      
    - **Example Files:**  
      Choose an example from the dropdown and click **Load Example** to pre-load sample assembly code.
      
    - **Assemble:**  
      Click the **Assemble** button to convert your assembly code into machine code.  
      You can choose the output format (Hex or Binary) using the dropdown.
                
    - **Download:**
      Click the **Download Assembled Code** button to download the assembled code.
      
    - **Run CPU:**  
      Click the **Run CPU** button to simulate execution.  
      The CPU’s register values and memory content will be displayed below.
      
    **Instruction Set Overview:**
    - **mov / movu / movh:**  
      - `mov` copies data between registers or loads an immediate (default uses sign extension).  
      - `movu` loads an immediate value as unsigned (zero-extended).  
      - `movh` loads an immediate into the high half of the register.
    - **Arithmetic Operations:** `add`, `sub`, `mul`, `div`, `mod`
    - **Logical Operations:** `and`, `or`, `not`
    - **Shift Operations:** `lsl` (logical shift left), `lsr` (logical shift right), `asr` (arithmetic shift right)
    - **Branching:** `beq` (branch if equal), `bgt` (branch if greater than), `b` (unconditional branch)
    - **Memory Operations:** `ld` (load) ***Syntax ld r5, 200[r1]*** , `st` (store) ***Syntax st r1, 200[r1]***
    - **Subroutine Calls:** `call`, `ret`
    - **'Note:'** The memory function can only be used with the syntax  **st r2, 200[r0]** or through
                **ld r1, 200[r0]**.
    """)
