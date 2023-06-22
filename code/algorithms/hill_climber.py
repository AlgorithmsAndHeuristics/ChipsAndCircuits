from circuit import Circuit


class HillClimber():
    
    def __init__(self, circuit: Circuit) -> None:
        for netlist in circuit.netlists:
            # Sort nets by wire length from longest to shortest
            nets = sorted(netlist.nets2.values(), key=lambda net: len(net.wiring), reverse=True)
            
            for net in nets:
                print(f'\nlen(net.wiring): {len(net.wiring)}')
                
                for wire in net.wiring:
                    print(f'Wire: {wire}')

