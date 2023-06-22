from circuit import Circuit
from collections import defaultdict


class HillClimber():
    
    def __init__(self, circuit: Circuit) -> None:
        for netlist in circuit.netlists:
            # Sort nets by wire length from longest to shortest
            nets = sorted(netlist.nets2.values(), key=lambda net: len(net.wiring), reverse=True)
            
            for net in nets:
                print(f'Wiring (old): {net.wiring}')
                wiring = defaultdict(list)
                
                for wire in net.wiring:
                    # Group wiring by Z-coordinate
                    wiring[wire.z].append(wire)
                    
                # Shorten wiring by retaining the largest wiring group
                net.wiring = wiring[max(wiring, key=lambda wire: wire)]
                print(f'Wiring (new): {net.wiring}')
                
                # Temporary: Stop after the first wire
                break

