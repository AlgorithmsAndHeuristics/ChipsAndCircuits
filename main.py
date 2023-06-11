from code.classes import circuit
import pandas as pd

if __name__ == "__main__":
    chip = 0

    # Get all three paths to netlists
    paths_netlist = []
    for i in range(1, 4):
        netlist_path = f"./data/chip_{chip}/netlist_{chip * 3 + i}.csv"
        paths_netlist.append(netlist_path)

    # Get print_i path
    print_path = f"./data/chip_{chip}/print_{chip}.csv"

    # Create the circuit
    chip = circuit.Circuit(print_path)

    # Check circuit
    print(chip.get_representation())

    
