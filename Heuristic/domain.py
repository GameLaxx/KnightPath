# Copyright (c) AIRBUS and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from copy import deepcopy
from enum import Enum
from math import sqrt
from typing import Any, NamedTuple, Optional, List

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')  # Ou 'Qt5Agg' si vous avez PyQt5 installé

from skdecide import DeterministicPlanningDomain, Space, Value
from skdecide.builders.domain import Renderable, UnrestrictedActions
from skdecide.hub.space.gym import EnumSpace, ListSpace, MultiDiscreteSpace

def make_board(size):
    ret = []
    for _ in range(size):
        ret.append([])
        for _ in range(size):
            ret[-1].append(0)
    return ret
def copy_board(board):
    ret = []
    for row in board:
        new_row = row[::]
        ret.append(new_row)
    return ret

class State(NamedTuple):
    x: int
    y: int
    board : List[List[int]]
    path : List[List[int]]
    length : int

class Action(Enum):
    LLU = [-2, -1]
    LLD = [-2, 1]
    LUU = [-1, -2]
    LDD = [-1, 2]
    RRU = [2, -1]
    RRD = [2, 1]
    RUU = [1, -2]
    RDD = [1, 2]
    NO_MORE = [0,0]

class D(DeterministicPlanningDomain, UnrestrictedActions, Renderable):
    T_state = State  # Type of states
    T_observation = T_state  # Type of observations
    T_event = Action  # Type of events
    T_value = float  # Type of transition values (rewards or costs)
    T_predicate = bool  # Type of logical checks
    T_info = (
        None  # Type of additional information given as part of an environment outcome
    )

class CavalouDomain(D):
    def __init__(self, origin, n):
        self.length = n
        self.origin = State(origin[0], origin[1], make_board(n), [[origin[0], origin[1]]], 1)
        self.origin.board[origin[0]][origin[1]] = 1
        self.desire = 65
        self._ax = None
        self._image = None

    def _get_action_space(self) -> Space[D.T_event]:
        return EnumSpace(Action)
        
    def _get_applicable_actions_from(self, memory: D.T_state) -> Space[D.T_event]:
        space = [Action.NO_MORE]
        for elm in Action:
            new_x = memory.x +  elm.value[0]
            new_y = memory.y +  elm.value[1]
            if new_x < 0 or new_x >= self.length or new_y < 0 or new_y >= self.length:
                continue
            if memory.board[new_x][new_y] >= 1:
                continue
            space.append(elm)
        return ListSpace(space)

    def _get_next_state(
        self,
        memory: D.T_memory[D.T_state],
        action: D.T_agent[D.T_concurrency[D.T_event]],
    ) -> D.T_state:
        new_x = memory.x + action.value[0]
        new_y = memory.y + action.value[1]
        new_path = memory.path[::]
        new_path.append([new_x, new_y])
        new_state = State(new_x, new_y, copy_board(memory.board), new_path, memory.length + 1)
        new_state.board[new_x][new_y] += 1
        return new_state

    def _get_transition_value(
        self,
        memory: D.T_memory[D.T_state],
        action: D.T_agent[D.T_concurrency[D.T_event]],
        next_state: Optional[D.T_state] = None,
    ) -> D.T_agent[Value[D.T_value]]:
        if next_state.x == memory.x and next_state.y == memory.y:
            return Value(cost=5)
        return Value(cost=1)
    
    def _is_goal(self, observation: D.T_agent[D.T_observation]) -> D.T_agent[D.T_predicate]:
        return observation.length == self.desire

    def _is_terminal(self, state: D.T_state) -> D.T_agent[D.T_predicate]:
        return self.get_applicable_actions(state).get_elements() == [] or self._is_goal(state)

    def _get_initial_state_(self) -> D.T_state:
        return self.origin

    def _get_observation_space_(self) -> D.T_agent[Space[D.T_observation]]:
        return MultiDiscreteSpace(
            nvec=[self.length, self.length], element_class=State
        )

    def _render_from(self, memory: D.T_memory[D.T_state], **kwargs: Any) -> Any:
        if self._ax is None:
            # fig = plt.gcf()
            fig, ax = plt.subplots(1)
            # ax = plt.axes()
            ax.set_aspect("equal")  # set the x and y axes to the same scale
            plt.xticks([])  # remove the tick marks by setting to an empty list
            plt.yticks([])  # remove the tick marks by setting to an empty list
            ax.invert_yaxis()  # invert the y-axis so the first row of data is at the top
            self._ax = ax
            plt.ion()
        board = copy_board(memory.board)
        board[memory.x][memory.y] = 2
        if self._image is None:
            self._image = self._ax.imshow(board)
        else:
            self._image.set_data(board)
        # self._ax.pcolormesh(maze)
        # plt.draw()
        plt.pause(0.3)

    def heuristic(self, s: D.T_state) -> Value[D.T_value]:
        """Heuristic to be used by search algorithms.

        Here Euclidean distance to goal.

        """
        moves = len(self.get_applicable_actions(s).get_elements())
        return Value(cost=self.desire - s.length + moves - 8)