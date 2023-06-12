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

### Gate
Een component die door middel van connecties (**Net**s) aan andere gates verbonden moet worden. Bevat de volgende variabelen:
* **self.id**: een unieke identifier (integer);
* **self.position:** een tuple met een x en y coördianat (integers).

Bevat de volgende method(s):

* **get_distance(self, other_gate):** geeft de hemelsbrede afstand tussen self en de gegeven gate.

### Wire
Een draadcomponent in een **Net**. Bevat de volgende variabelen:
* **self.x:** een integer die de x coördinaat representeert;
* **self.y:** een integer die de y coördinaat representeert.

### Intersection
Een overlap tussen twee **Net**s. Bevat de volgende variabelen:
* **self.net1:** een Net object dat met net2 overlapt;
* **self.net2:** een net object dat met net1 overlapt;
* **self.x:** een integer die de x coördinaat representeert;
* **self.y:** een integer die de y coördinaat representeert.

### Circuit
Een canvas met **Gate**s en **Netlist**s. Bevat de volgende variabelen:
* **self.netlists:** een lijst met Netlist objects;
* **self.gates:** een lijst met Gate objects.

Bevat de volgende methode(s):
* **self.make_grid(self, factor):** maakt een grid met een oppervlakte afhankelijk van de gegeven factor.

Het printen van een **Circuit** object geeft een array waar lege plekken weergegeven worden met een **underscore**, gates met hun **id**, draden met een **punt** en intersecties met een **x**. 

# Algorithms
De algorithms folder bevat de diverse algoritmes om het probleem op te lossen. In deze folder vind je:
