from circuit import Circuit


class HillClimber():
    
    def __init__(self, circuit: Circuit) -> None:
        self.circuit = circuit


    def make_incremental_change(self) -> None:
        for netlist in self.circuit.netlists:
            print(f"Wire count: {netlist.get_wire_count()}")
            
            for _, net in netlist.nets2.items():
                for wire in net.wiring:
                    print(f"Wire: {wire}")
                    break
                    
                break
            
            break
