import os, sys
from stopit import threading_timeoutable as timeoutable

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

from circuit import Circuit
from randomise import make_nets
from manhattan_path import make_manhattan_connection

# Attempt to lay the nets within the given time limit
# Adds the cost values to costs.txt
@timeoutable()
def make_net_timed(circuit, chip_id, netlist_id, plot: bool = False, write: bool = False):

    make_nets(circuit = circuit, netlist_id = netlist_id)

    print(f"Configuration cost: {sum([netlist.get_cost() for netlist in circuit.netlists])}")

    if write:
        with open('code/experiments/baseline_costs.txt', "a") as file:
                file.write(f'{sum([netlist.get_cost() for netlist in circuit.netlists])}\n')

    if plot:
        print(f"Plotting grid:")
        return circuit.plot_grid("Chip {chip}, Netlist {netlist_id}")


if __name__ == "__main__":

    print("Please select which chip you'd like to use.\n")
    for i in range(3): print(f"Enter {i} to use chip_{i}")

    # Prompt for the chip specification
    while True:
        chip = int(input("> "))

        if chip in range(3):
                break

    print(f"\nPlease select which netlist you'd like to use\n")
    for i in range(3): print(f"Enter {chip * 3 + i + 1} to use netlist_{chip * 3 + i + 1}")

    # Prompt for the netlist specification
    while True:
            netlist_id = int(input("> "))

            if netlist_id in range(chip * 3 + 1,  chip * 3 + 4):
                break

    print("\nPlease select which baseline algorithm you'd like to use.\n\
Enter 0 to use the manhattan path algorithm.\n\
Enter 1 to use the random path algorithm.\n")
    
    if chip > 0: print("Please note that running random path on chip_1 or chip_2 will likely take \
                       incredibly long.\n It is recommended to only run this algorithm on chip_0")
    
    # Prompt for the algorithm specification
    while True:
        chosen_algorithm = int(input("> "))

        if chosen_algorithm in range(2):
            break

    if chosen_algorithm == 1:
        print("Would you like to run the algorithm in plot mode or experiment mode?\n\
Enter 0 for plot mode: The algorithm is run once and the resulting configuration gets presented in a plot.\n\
Enter 1 for experiment mode: The algorithm is run a prompted number of times \
and the cost gets written to experiments/baseline_costs.txt.\n")

        while True:
            chosen_mode = int(input("> "))

            if chosen_mode in range(1):
                break

        # Ask for a run count in case of experiment mode
        if chosen_mode == 1:
            plot = False
            write = True

            print("How many times would you like to run the algorithm? Please enter a positive, whole number.")

            # Prompt for test count
            while True:
                run_count = int(input("> "))

                if type(run_count == int):
                    break
        else:
            run_count = 1
            plot = True
            write = False
    else:
        run_count = 1
        plot = True

    # Run the algorithm the specified amount of times
    for i in range(run_count):

        # Random path:
        if chosen_algorithm == 1:
            circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv", border = 15)
            circuit.load_netlist(f"data/chip_{chip}/netlist_{netlist_id}.csv")
            make_net_timed(timeout = 30, circuit = circuit, chip_id = chip, 
                           netlist_id = netlist_id, plot = plot, write = write)
        
        # Manhattan
        else: 
            circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")
            circuit.load_netlist(f"data/chip_{chip}/netlist_{netlist_id}.csv")

            for net in circuit.netlists[0].nets2.values():
                make_manhattan_connection(net)

            circuit.plot_grid("Chip 0, Netlist 1")



        


        
    
