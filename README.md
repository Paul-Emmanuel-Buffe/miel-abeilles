# Honey and Bees – Optimization with Genetic Algorithms

**Contributors:** Paul-Emmanuel Buffe, Yannis Messadia

---

## Project Context
This project applies **genetic algorithms** to optimize bee foraging behavior. A **colony of 101 bees** (including the queen) settled in a **wild apple tree** at the center of a field of **dandelions and meadow sage**.

Objective: **maximize foraging efficiency** by minimizing the total distance traveled while visiting all flowers.

---

## Technical Goals
- Implement a **genetic algorithm** for the Traveling Salesman Problem (TSP) variant.
- Maintain a constant population of 100 bees + 1 queen.
- Generate a **complete bee log** (`bees_log.csv`) for tracking and analysis.
- Study the impact of parameters (`mutation_rate`, `elitism_rate`, `crossover_method`) on overall performance.
- Provide clear visualizations accessible to non-technical users via `visuals.py` and `colony.ipynb`.

---

## Project Structure
```
.
|-- README.md
|-- main.py
|-- bee_count.py
|-- genealogy.py
|-- selection_rules.py
|-- utils.py
|-- visuals.py
|-- bees_log.csv
|-- colony.ipynb
```
- **main.py** – main simulation script  
- **bee_count.py** – bee management and logging  
- **genealogy.py** – bee genealogy tree  
- **selection_rules.py** – crossover and reproduction logic  
- **utils.py** – utility functions (distance, mutation, random path generation)  
- **visuals.py** – visualization of paths and trees  
- **bees_log.csv** – simulation output data  
- **colony.ipynb** – interactive analysis of performance and parameter impact  

---

## Data File – `bees_log.csv`
| Column            | Description |
|------------------|-------------|
| `id`             | Unique bee ID |
| `simulation_id`  | Simulation number |
| `generation`     | Bee generation |
| `distance`       | Total path distance |
| `parent_1`, `parent_2` | IDs of parents (if any) |
| `chemin`         | List of flower indices visited |
| `n_generations`  | Total number of simulated generations |
| `mutation_rate`  | Mutation rate applied |
| `elitisme_rate`   | Elitism rate applied |
| `crossover_method` | Crossover method used |
| `timestamp`      | Creation date and time |

This file allows **statistical analysis** and visualization of colony evolution.

---

## Genetic Algorithm – Conceptual Flow
```
Initial Generation (random paths)
|
Fitness Evaluation (total distance)
|
Parent Selection (elitism_rate)
|
Crossover (crossover_method)
|
Mutation (mutation_rate)
|
New Generation (replace least fit)
|
Repeat for n_generations
```

---

## Bee Genealogy
- Each node = a bee  
- Parent to child links = transmission of optimal paths  
- Visualizes the **evolution of field knowledge** over generations  
- Accessible interactively via `visuals.py` using `plot_classic_tree(tree, bee_id)`  

---

## Parameter Analysis
- **`mutation_rate`**: too low leads to stagnation, too high creates instability  
- **`elitism_rate`**: too low loses best paths, too high reduces diversity  
- **`crossover_method`**: affects inheritance of good path segments  

Analysis is implemented in **`colony.ipynb`**, which compares parameters and visualizes their impact on:  
- Minimum distance of the best bee  
- Average distance per generation  
- Standard deviation and stability of paths  

---

## Comparative Performance Analysis of Genetic Algorithms

### Objectives and Initial Hypotheses
This analysis compared two crossover operators within the genetic algorithm framework for the traveling salesman problem:
- **Order Crossover** (OX)
- **Common Edges Crossover** (CEX)

Initial hypotheses:
1. Common Edges Crossover would converge faster initially
2. Order Crossover would produce superior final solutions
3. Mutation rate impact would be minimal between 0.1 and 0.5

### Key Results

**Algorithm Comparison**  
Results demonstrate clear superiority of **Order Crossover**:

| Metric | Order Crossover | Common Edges | Interpretation |
|--------|-----------------|--------------|----------------|
| **Average final distance** | 9,955 | 22,073 | 2x shorter paths |
| **Area under curve (AUC)** | 1.27M | 2.30M | Better learning |
| **95% convergence** | Generation 69 | Generation 94 | Faster |
| **Run variance** | ~550k | ~1.35M | More stable |

**Statistical Testing**  
Observed differences are **highly significant**:
- **Welch's t-test**: t = -35.753, p = 2.031e-14
- **Mann-Whitney test**: U = 0.0, p = 1.827e-04
- **Cohen's d effect size**: d = -15.989 (very strong effect)

**Mutation Rate Impact**  
Contrary to initial assumptions, mutation rate shows **significant impact** on performance. Visual analysis of performance curves reveals notable variations across tested mutation rates (0.1, 0.2, 0.3, 0.5).

### Performance Visualizations
Graphical analyses highlight:
- **Average distance evolution**: Order Crossover maintains consistent advantage from early generations
- **Direct method comparison**: Order Crossover curve remains systematically below Common Edges
- **Mutation rate impact**: Different curves demonstrate sensitivity of both methods to mutation rate variations

### Conclusions
1. **Order Crossover clearly outperforms Common Edges** across all performance indicators
2. **Mutation rate hypothesis rejected** – this parameter significantly influences results
3. Methodology enabled **rigorous scientific comparison** of algorithms
4. Genetic approach proved effective for modeling solution evolution

This analysis demonstrates the importance of crossover operator selection in genetic algorithms and emphasizes the necessity of empirical parameter evaluation rather than relying on initial intuitions.

---

## Complementary Heuristic Algorithms
1. **Simulated Annealing** – accepts temporarily worse solutions to escape local minima  
2. **Particle Swarm Optimization (PSO)** – collective movement toward best positions  
3. **Tabu Search** – systematic exploration with memory of forbidden moves  

---

## Visualizations
- `plot_best_path(fleurs, best_chemin)` – shows the optimal path  
- `plot_avg_distance(avg_distances, n_generations)` – shows evolution of performance  
- `plot_classic_tree(tree, bee_id)` – interactive genealogy tree  

---

## Dependencies
- `numpy`  
- `pandas`  
- `matplotlib`  

---

## Usage
1. **Run the simulation**:  
```bash
python main.py
```

2. **Explore genealogy and paths**:
```bash
python visuals.py
```
