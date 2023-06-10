# Classes
De classes folder bevat de diverse classes die gebruikt worden om het probleem en de oplossing te representeren. In deze folder vind je:

## netlist.py
Bevat de Net en Netlist classes.

### Net
Een connectie tussen twee **Gates**. Bevat de volgende variabelen:
* **self.gates**: een tuple met de IDs van de twee gates die door het net verbonden dienen te worden;
* **self.wiring**: een lijst met tuples bestaande uit een x en y coördinaat die de positie van de wire fragmenten aangeeft.

Bevat de volgende methods:
* **add_wire(self, x, y): voegt een wire fragment toe aan self.wiring**

### Netlist
Een collectie **Nets**. Bevat de volgende variabelen:
* **self.nets:** een lijst met **Net** objects.

Bevat de volgende methods:
* **get_wire_count(self):** geeft het totale aantal draad fragmenten in net.wiring for alle nets in de netlist;
* **get_intersections(self):** geeft een lijst met alle kruisende **nets** en de coördinaten van de kruising;
* **get_cost(self):** geeft de cost waarde.

# Algorithms
De algorithms folder bevat de diverse algoritmes om het probleem op te lossen. In deze folder vind je:
