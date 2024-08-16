import numpy as np


def play_match(exp_home: float, exp_visitor: float, dispar: float) -> list[int]:
    """ Simulates the result of a match using Poison distribution
    Arguments:
        exp_home: a float meaning the average points of home team
        exp_visitor: a float meaning the average points of the visitor team
        dispar: a float to twist things in favor of home team
    Returns:
        A list of two integers with the simulated match result
    """
    lambda_home = exp_home * (1 + (dispar / 2))
    lambda_visit = exp_visitor * (1 - (dispar / 2))
    pts_home = np.random.poisson(lambda_home)
    pts_visit = np.random.poisson(lambda_visit)
    return [pts_home, pts_visit]
