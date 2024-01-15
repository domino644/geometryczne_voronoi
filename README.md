# "Comparison of Voronoi diagrams construction methods"

### Made by Jakub Ciszewski and Olaf Fertig

The project was created as part of geometric algorithms at AGH.
It contains 3 algorithms for constructing a Voronoi diagram:

1. Naive algorithm - made by Olaf Fertig
2. Algorithm that constructs diagram from Delauney triangulation - made by Olaf Fertig
3. Fortune's Algorithm - made by Jakub Ciszewski; this is basically python copy of [this code](https://github.com/pvigier/MyGAL/blob/master/include/MyGAL/Box.h).

Fortune's algorithm source code is in `modules` folder. Naive and triangulation algorithm source code is in `main.ipynb` as well as all the examples and visualisations.

Visualisation is supportd by [AGH BIT](https://github.com/aghbit) tool -`Visualizer`.

Documentation and presentation are available only in Polish language.

## Requirements:

1. `python >=3.10.11`
2. `scipy`
3. `matplotlib`
4. `pandas`
5. `numpy`
