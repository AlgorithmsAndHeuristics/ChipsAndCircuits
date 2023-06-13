# Classes
De classes folder bevat de diverse classes die gebruikt worden om het probleem en de oplossing te representeren. In deze folder vind je:

## netlist.py
Bevat de Net en Netlist classes.

### Net
Een connectie tussen twee **Gate**s. Bevat de volgende variabelen:
* **self.gates**: een tuple met de IDs van de twee gates die door het net verbonden dienen te worden;
* **self.wiring**: een lijst met tuples bestaande uit een x en y coördinaat (integers) die de positie van de wire fragmenten aangeeft.

Bevat de volgende method(s):
* **add_wire(self, x, y):** voegt een wire fragment toe aan self.wiring
* **get_wire_positions(self):** geeft een lijst van tuples met de x en y coördinaten (integers) van alle wires van het net.

### Netlist
Een collectie **Net**s. Bevat de volgende variabelen:
* **self.nets:** een lijst met **Net** objects.

Bevat de volgende method(s):
* **get_wire_count(self):** geeft het totale aantal draad fragmenten in net.wiring for alle nets in de netlist;
* **check_intersection(self, net2):** geeft true als er een intersectie is tussen self en net2. Anders false;
* **get_intersections(self):** geeft een lijst met alle kruisende **nets** en de coördinaten van de kruising;
* **get_cost(self):** geeft de cost waarde als integer.

## gate.py
Bevat de Gate class.

### Gate
Een component die door middel van connecties (**Net**s) aan andere gates verbonden moet worden. Bevat de volgende variabelen:
* **self.id**: een unieke identifier (integer);
* **self.position:** een tuple met een x en y coördianat (integers).

Bevat de volgende method(s):

* **get_distance(self, other_gate):** geeft de hemelsbrede afstand tussen self en de gegeven gate.

## wire.py
Bevat de Wire class

### Wire
Een draadcomponent in een **Net**. Bevat de volgende variabelen:
* **self.x:** een integer die de x coördinaat representeert;
* **self.y:** een integer die de y coördinaat representeert.

## intersection.py
Bevat de Intersection class

### Intersection
Een overlap tussen twee **Net**s. Bevat de volgende variabelen:
* **self.net1:** een Net object dat met net2 overlapt;
* **self.net2:** een net object dat met net1 overlapt;
* **self.x:** een integer die de x coördinaat representeert;
* **self.y:** een integer die de y coördinaat representeert.

## circuit.py
Bevat de Circuit class

### Circuit
Een canvas met **Gate**s en **Netlist**s. Bevat de volgende variabelen:
* **self.netlists:** een lijst met Netlist objects;
* **self.gates:** een lijst met Gate objects.

Bevat de volgende methode(s):
* **self.make_grid(self, factor):** maakt een grid met een oppervlakte afhankelijk van de gegeven factor.
* **self.check_position(self, x, y):** geeft een triple met booleans die respectievelijk aangeven of de positie met de gegeven coördinaten buiten de range van de grid is, een Gate bevat of een Wire bevat.

Het printen van een **Circuit** object geeft een array waar lege plekken weergegeven worden met een **underscore**, gates met hun **id**, draden met een **punt** en intersecties met een **x**. 

# Algorithms
De algorithms folder bevat de diverse algoritmes om oplossingen voor het Chips & Circuits probleem te vinden. In deze folder vind je:

## random.py
Bevat de code voor ons baseline algoritme: **Random Path**. Dit algoritme werkt als volgt:
![Random Path Flowchart](../images/random_path_flowchart.png)

random.py bevat de volgende functies:

* **wire_net(circuit, net):** maakt de draden voor een gegeven Net aan door willekeurige, valide posities te kiezen. Begin opnieuw als de draad vast komt te zitten.
