import os, sys, time
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
def make_net_timed(circuit, chip_id, netlist_id, plot: bool = False):
    """
    PRE: circuit object, chip_id, netlist_id and boolean for grid plotting.
    POST: Runs random algorithm on the circuit returns plot or bool indicating the run was succesful.
    """

    make_nets(circuit = circuit, netlist_id = netlist_id)

    print(f"Configuration cost: {sum([netlist.get_cost() for netlist in circuit.netlists])}")

    if plot:
        print(f"Plotting grid:")
        return circuit.plot_grid(f"Chip {chip}, Netlist {netlist_id}")

    else:
        return True


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

        # Set border sizes depending on the chosen chip
        if chip == 0:
             border = 8
        elif chip == 1:
             border = 17
        elif chip == 2:
             border = 17

        print("Would you like to run the algorithm in plot mode or experiment mode?\n\
Enter 0 for plot mode: The algorithm is run once and the resulting configuration gets presented in a plot.\n\
Enter 1 for experiment mode: The algorithm is run for a prompted duration \
and the cost gets written to experiments/baseline_costs.txt.\n")

        while True:
            chosen_mode = int(input("> "))

            if chosen_mode in range(2):
                break

        # Ask for a run count in case of experiment mode
        if chosen_mode == 1:

            plot = False
            write = True

            print("For how many seconds would you like to run the algorithm? Please enter a positive, whole number.")

            # Prompt for test count
            while True:
                total_time = int(input("> "))

                if type(total_time == int):
                    break
        else:
            total_time = 60
            plot = True
            write = False
    else:
        plot = True

    
    # Random path:
    if chosen_algorithm == 1:
        
        start_time_global = time.time()
        
        # Run for the specified duration
        while time.time() - start_time_global < total_time:
            
            # Time each run
            start_time_local = time.time()

            circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv", border = border)
            circuit.load_netlist(f"data/chip_{chip}/netlist_{netlist_id}.csv")

            # Write the data to the file if the netlist was completed within the given time
            if make_net_timed(timeout = 60, circuit = circuit, chip_id = chip, 
                            netlist_id = netlist_id, plot = plot) == True:
                
                # Write the cost and excecution runtime to the file
                with open('code/experiments/baseline_costs01.txt', "a") as file:
                        cost = sum([netlist.get_cost() for netlist in circuit.netlists])
                        visited_states = sum([net.state_counter for net in circuit.netlists[0].nets.values()])
                        file.write(f'{cost},{time.time() - start_time_local},{visited_states}\n')
            
            if chosen_mode == 0:
                 break
            # Wait 1 second for safety
            time.sleep(1)

    # Manhattan
    else: 
        start_time_local = time.time()

        circuit = Circuit(f"data/chip_{chip}/print_{chip}.csv")
        circuit.load_netlist(f"data/chip_{chip}/netlist_{netlist_id}.csv")

        for net in circuit.netlists[0].nets.values():
            make_manhattan_connection(net)

        print(f"Runtime: {time.time() - start_time_local}")
        print(f"States visited: {sum([net.state_counter for net in circuit.netlists[0].nets.values()])}")


        circuit.plot_grid(f"Chip {chip}, Netlist {netlist_id}")

