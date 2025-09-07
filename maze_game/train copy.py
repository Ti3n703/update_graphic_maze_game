import neat 
import gymnasium
import numpy as np
import pickle

# Replace with your environment
import gym_env 
env = gym_env.EvnMaze

# ------------------------
# Define fitness function
# ------------------------
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitness = 0.0
    obs = env.reset()
    done = False
    max_steps = 500  # adjust as needed

    for _ in range(max_steps):
        # Flatten obs if necessary
        if isinstance(obs, np.ndarray) and obs.ndim > 1:
            obs = obs.flatten()
        action_values = net.activate(obs)
        action = np.argmax(action_values)  # discrete action
        obs, reward, done, _ = env.step(action)
        fitness += reward
        if done:
            break
    return fitness

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

# ------------------------
# Load NEAT config
# ------------------------
config_path = "config-feedforward.txt"  # create this file
config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    config_path
)

# ------------------------
# Create population
# ------------------------
pop = neat.Population(config)

# Add reporters (optional)
pop.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

# ------------------------
# Run NEAT
# ------------------------
winner = pop.run(eval_genomes, n=100)  # n = generations

# ------------------------
# Save best genome
# ------------------------
with open('best_genome.pkl', 'wb') as f:
    pickle.dump(winner, f)

print("Training complete. Best genome saved as best_genome.pkl")
