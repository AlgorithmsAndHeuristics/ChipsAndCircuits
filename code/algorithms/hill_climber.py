from circuit import Circuit
from collections import defaultdict


class HillClimber():
    
    def __init__(self, circuit: Circuit) -> None:
        for netlist in circuit.netlists:
            # Sort nets by wire length from longest to shortest
            nets = sorted(netlist.nets2.values(), key=lambda net: len(net.wiring), reverse=True)
            
            for net in nets:
                wiring = defaultdict(list)
                
                for wire in net.wiring:
                    # Group wiring by Z-coordinate
                    wiring[wire.z].append(wire)
                
                print(f'Wiring (z=0): {wiring[0]}')
                print(f'Wiring (z=1): {wiring[1]}')
                
                # Temporary: Stop after the first wire
                break

