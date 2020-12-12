# CellularLifeSimulator
## Summary
This program uses a simple algorithm to create a seemingly complex simulation of cellular organisms represented by a matrix.

## Parallelization 
The key feature of this program is its ability to use a scatter gather approach with processes to optimize performance. 


Texas Tech HPCC Run Time Results
| Size        | Threads | Result (sec) |
|------------ |-------------|--------|
|100x100 | 1| 1.5|
|100x100| 2| .9414|
|100x100|4|.7604|
|100x100|8|.7191|
|100x100|16|1.0978|
|100x100|32|1.3800|
|1000x1000| 1| 114.8|
|1000x1000| 2| 77.7|
|1000x1000|4|56.3|
|1000x1000|8|50.7|
|1000x1000|16|57.8|
|1000x1000|32|85.1|
|10000x10000 | 9| 3659.6|
|10000x10000| 18| 4881.3|
|10000x10000|36|7728.5|

## Simulation Algortihm
The Matrix is any rectangular matrix consisting of '.' and '0' 

1) Any position in the matrix with a period ‘.’ is considered “dead” during the current time step.
2) Any position in the matrix with a capital ‘O’ is considered “alive” during the current time step.
3) If an “alive” square has exactly two, three, or four living neighbors, then it continues to be “alive” in the
next time step.
4) If a “dead” square has an even number greater than 0 living neighbors, then it will be “alive” in the next
time step.
5) Every other square dies or remains dead, causing it to be “dead” in the next time step
