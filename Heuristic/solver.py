from time import sleep
from IPython.display import clear_output, display
import datetime

from matplotlib import pyplot as plt
from skdecide import Solver
from skdecide import utils
from skdecide.hub.solver.astar import Astar
from typing import Optional

from domain import CavalouDomain, State

domain_factory = lambda: CavalouDomain([4,4], 8)
# instanciate the domain
domain = domain_factory()
# init the start position
initial_state = domain.reset()
# domain.render(initial_state)


def rollout(
    domain: CavalouDomain,
    solver: Solver,
    max_steps: int,
    pause_between_steps: Optional[float] = 0.01,
):
    """Roll out one episode in a domain according to the policy of a trained solver.

    Args:
        domain: the maze domain to solve
        solver: a trained solver
        max_steps: maximum number of steps allowed to reach the goal
        pause_between_steps: time (s) paused between agent movements.
          No pause if None.

    """
    # Initialize episode
    solver.reset()
    observation = domain.reset()

    # Initialize image
    figure = domain.render(observation)
    display(figure)

    # loop until max_steps or goal is reached
    for i_step in range(1, max_steps + 1):
        if pause_between_steps is not None:
            sleep(pause_between_steps)

        # choose action according to solver
        action = solver.sample_action(observation)
        # get corresponding action
        outcome = domain.step(action)
        observation = outcome.observation
        # update image
        figure = domain.render(observation)
        clear_output(wait=True)
        # display(figure)

        # final state reached?
        if domain.is_terminal(observation):
            break

    # goal reached?
    is_goal_reached = domain.is_goal(observation)
    if is_goal_reached:
        print(f"Goal reached in {i_step} steps!")
    else:
        print(f"Goal not reached after {i_step} steps!")

    return is_goal_reached

max_steps = 800
solver = Astar(domain_factory=domain_factory, heuristic=lambda d, s: d.heuristic(s))
solver.solve()
print("Done solving !")
rollout(domain=domain, solver=solver, max_steps=max_steps, pause_between_steps=None)
plt.pause(10)
# test = State(x=7, y=0, board=[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0], [1, 1, 0, 0, 1, 1, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]], path=[[7, 7], [6, 5], [7, 3], [6, 1], [5, 3], [7, 4], [6, 6], [5, 4], [6, 2], [4, 1], [6, 0], [7, 2], [6, 4], [7, 6], [5, 7], [4, 5], [2, 4], [3, 6], [4, 4], [5, 6], [7, 5], [6, 7], [5, 5], [6, 3], [7, 1], [5, 2], [4, 0], [3, 2], [5, 1], [7, 0]], length=30)
# domain.render(test)