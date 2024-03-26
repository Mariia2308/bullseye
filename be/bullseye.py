"""Bullseye

Write a proper docstring here such that:
    - if the flag `--seed SEED` is provided, the seed SEED should be used to generate random numbers
    - if the flag `--games GAMES` is provided, the program should run GAMES number of games

Have a look at https://docopt.org on how to do this

Usage:
  bullseye [--seed=<SEED>] [--games=<GAMES>]
  bullseye -h | --help
  bullseye --version

Options:
  --seed=<SEED>   Seed for random number generation.
  --games=<GAMES> Number of games to run.

  -h --help       Show this screen.
  --version       Show version.

"""

import numpy as np
from docopt import docopt

__version__ = "0.2.0"

def get_opts():
    """Get the options passed to the program via docopt.

    Returns:
        options (dict): A dictionary with the options.
    """
    opts = docopt(__doc__, version=__version__)
    return opts

def update(x, y, r):
    """Update the radius according to the rules of the game.

    If the hit is on the disk, i.e. :math:`x_i**2+y_i**2 <= r_i**2`, the new radius
    :math:`r_{i+1}` will be the length of the side opposing
    :math:`\sphericalangle O-\left(x,y\right)-B` in the right triangle :math:`\Delta
    O-\left(x,y\right)-B`, where :math:`O` is the origin of the circle,
    :math:`\left(x, y\right)` the position the dart hit and :math:`B` the point
    intersecting the circle and the line perpendicular to
    :math:`\vec{O\left(x,y\right)}`.

    The radius must not shrink if we hit the bullseye. If we hit the center of the dartboard precisely, i.e. hit (0, 0), the
    radius should remain the same.

    The radius must be zero if we hit the border.`  
    Args:
      x (float): x coordinate of the dart
      y (float): y coordinate of the dart
      r (float): the radius of the dart board

    Returns:
        (float): the new radius if the disk was hit, 0 if hit the border, -1 otherwise
    """
    distance_squared = x**2 + y**2

    if distance_squared < r**2:
        if x == 0 and y == 0:
            return r  
        else:      
            new_radius = np.sqrt(x**2 + y**2)
            return new_radius
    else:
        if distance_squared == r**2:
            return 0
        else:
            return -1

def game():
    """One game of hitting the dart board until we miss

    First, we set the radius to 1, as this is the radius of the disk we want to start with.
    We also initialize a new variable to keep track of the score, i.e. the number of darts thrown until
    the board was missed (including the dart that missed). So, for example, if the first dart already misses the disk,
    the score should still be 1.

    Then, until we missed, we throw to a random point (x, y), update the radius using the update function above and increase the score by one.
    When a dart misses the board, the game ends and the final score is returned.

    Returns:
      score (int): the number of darts thrown.
    """
    radius = 1
    score = 0

    while True:
        x, y = np.random.uniform(-1, 1, 2) 
        score += 1
        new_radius = update(x, y, radius)

        if new_radius == -1:
            break

        radius = new_radius

    return score

def main(opts, games=10):
    """for a given number of games, record the scores, then return the mean and
    of the scores
    If the options contain a seed for the random number generator, pass this seed to numpy
    If the options contain a number of games to be played, play the game this many times

    Args:
      games (int): the number of games to play.

    Returns:
      mean (float):  the mean value of the scores
    """
     
    if opts  != None:
        if opts["--seed"]  != None:
            try:
                np.random.seed(int(opts["--seed"]))
            except:
                print("bbbb")

    scores = []

    for _ in range(games):
        score = game()
        scores.append(score)


    mean_score = np.mean(scores)
    return mean_score

if __name__ == "__main__":
    opts = get_opts()
    mean = main(opts, int(opts["--games"] or 100000))
    print(f"exp(pi/4) approx equal to {mean}")
