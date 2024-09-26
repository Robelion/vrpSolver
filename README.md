# Vehicle Routing Problem (VRP) Solver

This program solves a version of the Vehicle Routing Problem (VRP) using a combination of heuristics, including Greedy Savings and Simulated Annealing.

The VRP specifies a set of loads to be completed efficiently by an unbounded number of drivers. This solution takes a text file path describing a VRP as a command line argument, and writes a solution to stdout. The VRP solution contains a list of drivers, each of which has an ordered list of loads to be completed. All loads get assigned to a driver.

## Instructions on how to run `vrp_Solver.py` in the terminal:

1. Install python3.x.
2. Run the following command:

   ```bash
   python3 vrp_Solver.py {path_to_problem}
   ```

   - Replace `{path_to_problem}` with a path to the text file containing loads. If the text file (e.g. `problem1.txt`) is in the same directory as `vrp_Solver.py` then it would look like this:

     ```bash
     python3 vrp_Solver.py problem1.txt
     ```

   - The text file should have a format similar to this:

     ```
     loadNumber  pickup       dropoff
     1           (-50.1,80.0) (90.1,12.2)
     2           (-24.5,-19.2) (98.5,1.8)
     3           (0.3,8.9)    (40.9,55.0)
     4           (5.3,-61.1)  (77.8,-5.4)
     ```

## Reference to external sources:

1. [https://www.sciencedirect.com/science/article/abs/pii/S0096300313004001](https://www.sciencedirect.com/science/article/abs/pii/S0096300313004001)
2. [https://www.sciencedirect.com/science/article/abs/pii/S1568494610001304](https://www.sciencedirect.com/science/article/abs/pii/S1568494610001304)
3. [https://www.researchgate.net/publication/222077869_Simulated_annealing_algorithm_with_adaptive_neighborhood](https://www.researchgate.net/publication/222077869_Simulated_annealing_algorithm_with_adaptive_neighborhood)