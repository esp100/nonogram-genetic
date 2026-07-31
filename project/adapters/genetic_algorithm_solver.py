import pandas as pd
import numpy as np
from project.domain.nonogram_solver_port import NonogramSolverPort
from project.domain.entities import Nonogram
from itertools import zip_longest

class GeneticAlgorithmSolver(NonogramSolverPort):
    def solve(self, nonogram):
       
        row_hints, col_hints = nonogram.row_hints, nonogram.col_hints
                
        rows = len(nonogram.grid)
        cols = rows

        # Set modifiable parameters: population size, mutation rate, crossover rate, number of generations
        population_size = 100
        mutation_rate = 0.05
        crossover_rate = 0.9
        num_generations = 100000

        fitness_convergence =[]

        orthogonal_array = self.generate_orthogonal_array(rows)
    
        # Initial population

        population = self.initialize_population(population_size, rows, cols, row_hints)

        fitness_scores = [self.fitness_function(grid , col_hints) for grid in population]

        fitness_convergence.append( min(fitness_scores) )
        best = population[fitness_scores.index(min(fitness_scores))]

        if fitness_convergence[-1] == 0:
            return 1, fitness_convergence, population, best

        for generation in range(num_generations):
            print(f'generation ',generation,' ft ', fitness_convergence[-1])  
            new_population = [] 

            #Roulette selection     
            selected_population = list(self.roulette_wheel_selection(population, fitness_scores, crossover_rate))

            #crossover
            for i in range(0, len(selected_population), 2):
                parent_a = selected_population[i] 
                parent_b = selected_population[i+1] if i + 1 < len(selected_population) else parent_a
                child_a, child_b = self.cross_over(parent_a, parent_b)
                new_population.extend([child_a, child_b])

            #Taguchi offspring
            new_population = self.taguchi_offpring(new_population, col_hints, orthogonal_array)

            for m in range(len(new_population) - 1):
                if np.random.rand() < mutation_rate: 
                    new_population[m] = self.mutation( new_population[m], cols, row_hints)

            population = new_population
            fitness_scores = [self.fitness_function(grid , col_hints) for grid in population]

            fitness_convergence.append( min(fitness_scores) )
            if fitness_convergence[-1] > fitness_convergence[-2]:
                population[fitness_scores.index(max(fitness_scores))] = best
                fitness_scores = [self.fitness_function(grid , col_hints) for grid in population]

            best = population[fitness_scores.index(min(fitness_scores))]
            mutation_rate += 0.000001
            if fitness_convergence[-1] == 0: 
                return (generation+1), fitness_convergence, population, best
            
        return num_generations, fitness_convergence, population, best
        

    def generate_hints(self, grid):
        grid_df = pd.DataFrame(grid)

        row_hints = []
        col_hints = []

        for index, row in grid_df.iterrows():
            hints_aux = []
            count_aux = 0
            for cell in row:
                if cell == 1:
                    count_aux += 1
                else:
                    if count_aux > 0:
                        hints_aux.append(count_aux)
                        count_aux = 0
            if count_aux > 0:
                hints_aux.append(count_aux)
            elif len(hints_aux) == 0: 
                hints_aux.append(0)
            row_hints.append(hints_aux)

        for index, col in grid_df.items():
            hints_aux = []
            count_aux = 0
            for cell in col:
                if cell == 1:
                    count_aux += 1
                else:
                    if count_aux > 0:
                        hints_aux.append(count_aux)
                        count_aux = 0
            if count_aux > 0:
                hints_aux.append(count_aux)
            elif len(hints_aux) == 0: 
                hints_aux.append(0)
            col_hints.append(hints_aux)

        return row_hints, col_hints

    def validate_solution(self, nonogram):
        pass

    def fitness_function(self, grid, col_hints):
        fitness_score = 0
        grid_arr = np.asarray(grid)
        
        for index, col in enumerate(grid_arr.T):
            desired_numbers = col_hints[index]
            
            padded = np.pad(col, (1, 1), constant_values=0)
            diffs = np.diff(padded)
            starts = np.where(diffs == 1)[0]
            ends = np.where(diffs == -1)[0]
            consecutive = ends - starts
            
            for d, c in zip_longest(desired_numbers, consecutive, fillvalue=0):
                fitness_score += abs(d - c)

        return fitness_score

    def initialize_population(self, population_size, rows, cols, row_hints):
        population = []
        rng = np.random.default_rng()
        for _ in range(population_size):
            chromosome = np.zeros((rows, cols), dtype=int)
            for row_index, hints in enumerate(row_hints):
                encoded_row = self.generate_random_row(cols, hints, rng)
                chromosome[row_index] = self.decode_line(encoded_row, cols, hints)
            population.append(chromosome)
        return population

    def generate_random_row(self, cols, hints, rng):
        if len(hints) == 0 or hints == [0]:
            return np.zeros(cols, dtype=int)

        number_of_condensed = len(hints)
        zeros = cols - sum(hints)

        posiciones_base = rng.choice(zeros + 1, size=number_of_condensed, replace=False)
        
        posiciones_base.sort()
        
        posiciones_finales = posiciones_base + np.arange(number_of_condensed)
        
        row = np.zeros(zeros + number_of_condensed, dtype=np.int8)
        row[posiciones_finales] = 1

        return row

    def decode_chromosome(self, chromosome, rows, cols, row_hints):
        grid = np.zeros((rows, cols), dtype=int)
        for row_index, row in enumerate(chromosome):
            grid[row_index] = self.decode_line(row, cols, row_hints[row_index])
        return grid

    def decode_line(self, line, cols, hints):
        if len(line) == cols:
            return line
        else:
            repeats = np.ones(len(line), dtype=int)
            repeats[line == 1] = hints
            return np.repeat(line, repeats)

    def roulette_wheel_selection(self, population, fitness_scores, crossover_rate):
        reciprocal_fitness_scores = [1 / (score + 1e-6) for score in fitness_scores]
        total_fitness = sum(reciprocal_fitness_scores)
        for i in range(len(population)):
            if np.random.rand() < crossover_rate:
                selection_probs = [score / total_fitness for score in reciprocal_fitness_scores]
                selected_index = np.random.choice(len(population), p=selection_probs)
                yield population[selected_index]
            else:
                yield population[i]

    def cross_over(self, parent_a, parent_b):
        cross_point = np.random.default_rng().integers(0, len(parent_a))
        return np.vstack((parent_a[:cross_point], parent_b[cross_point:])), np.vstack((parent_b[:cross_point], parent_a[cross_point:]))

    def mutation(self, chromosome, cols, row_hints):
        rng = np.random.default_rng()
        mutated_line = rng.integers(0, len(chromosome))
        for _ in range(cols):
            if row_hints[mutated_line]==[0] :
                mutated_line = rng.integers(0, len(chromosome))
            else:
                break
        new_row = self.generate_random_row(cols, row_hints[mutated_line], rng)         
        chromosome[mutated_line] = self.decode_line(new_row, cols, row_hints[mutated_line])

        return chromosome

    def hadamard(self, order):    
        if order & (order - 1):
            raise ValueError("Failed to generate a Hadamard array with value different than base 2.")

        H = np.array([[1]], dtype=np.int8)

        while H.shape[0] < order:
            H = np.block([
                [ H,  H],
                [ H, -H]
            ])

        return (H < 0).astype(np.int8)

    def generate_orthogonal_array(self, n_genes):
        rows = 1 << int(np.ceil(np.log2(n_genes + 1)))
        H = self.hadamard(rows)

        return H[:, 1:n_genes + 1]


    def taguchi_offpring(self, population, col_hints, orthogonal_array):
        rng = np.random.default_rng()
        u1, u2 = rng.integers(0, len(population), 2)
        population[u1], population[u2] = self.orthogonal_cross(population[u1], population[u2], col_hints, orthogonal_array)

        return population


    def orthogonal_cross(self, u1, u2, col_hints, orthogonal_array): 
        experiments = np.where(orthogonal_array[..., np.newaxis] == 0, u1[np.newaxis, ...], u2[np.newaxis, ...])
        scores = np.array([
            self.fitness_function(grid , col_hints) for grid in experiments
            ])

        mask0 = orthogonal_array == 0
        mask1 = ~mask0

        mean0 = (scores[:, None] * mask0).sum(axis=0) / mask0.sum(axis=0)
        mean1 = (scores[:, None] * mask1).sum(axis=0) / mask1.sum(axis=0)

        return np.where(mean0 > mean1, u1, u2), np.where(mean0 > mean1, u1, u2)
            
