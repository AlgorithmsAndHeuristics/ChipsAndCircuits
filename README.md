# Chips and circuits

Hier staat een korte beschrijving van het probleem evt. met plaatje.

## Aan de slag (Getting Started)

### Vereisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.8.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

Alle Python scripts staan in de folder **code**. In de map **data** zitten alle input waardes en in de map **code/experiments** worden diverse resultaten van de code opgeslagen. In de map **images** staan de afbeeldingen voor de README bestanden.
Het bestand baseline.py bevat twee baseline algoritmes: random path en manhattan path. Het wordt wegens de zeer lange runtimes afgeraden random path op grotere chips dan chip 0 te runnen. Voor deze chips wordt manhattan path als baseline gebruikt.

### Test (Testing)

Om greedy of randomised greedy te draaien, gebruik je:

```
python main.py
```

Om random path en manhattan path te draaien, gebruik je: 

```
python baseline.py
```
Na het runnen van main.py of baseline.py wordt je door diverse tekst prompts door de run opties genavigeerd. Hierbij krijg je keuze tussen **plot modus** waar het algoritme één keer gerund wordt en de resultaten in een plot weergegeven worden, en **experiment modus** waar het algoritme gedurende een geprompte tijd runt en alle kosten, runtime en het aantal bezochte states aan _baseline_costs.txt_ of _main_costs.txt_ toegevoegd wordt.

Onze resultaten van alle algoritmes zijn te zien in code/experiments/experiments.ipynb

## Auteurs (Authors)

* Joey Blankendaal
* Lindel Pieters
* Matyas Wouters

## Dankwoord (Acknowledgments)

* StackOverflow
* minor programmeren van de UvA
