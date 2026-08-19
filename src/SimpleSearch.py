# Copyright 2018 Jose Ortiz-Bejar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Tree/Graph search following Russell & Norvig's pseudocode.
# Uninformed strategies (BFS, DFS) and informed search (A*) share the same
# loop; they only differ in (a) how the frontier is ordered and (b) how
# repeated states are discarded.

import heapq
from collections import deque


class Node:
    """A node of the search tree.

    state      problem state (tuple, string, vector...). Must be hashable.
    parent     node that generated this one (None for the root)
    depth      number of steps from the root                     [depth(n)]
    step_cost  cost of the single move parent -> this node       [c(parent,a,n)]
    cost       accumulated cost from the root                    [g(n)]
    delta      heuristic estimate to the goal                    [h(n)]
    op         name of the operation that generated this node
    """

    def __init__(self, state, parent=None, depth=0, cost=0, op="", delta=0,
                 step_cost=1):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost            # g(n), recomputed by the search
        self.delta = delta          # h(n), filled in by the search for A*
        self.op = op
        self.step_cost = step_cost  # cost of this single move (1 by default)

    def f(self):
        """Evaluation function f(n) = g(n) + h(n).

        For BFS/DFS delta is 0, so f(n) is just the accumulated cost.
        """
        return self.cost + self.delta

    def getPath(self):
        """Route from the root to this node, as [(state, op, depth), ...].

        We walk up through the parents (which gives the reversed path) and
        reverse the list once at the end, instead of inserting at position 0
        on every step.
        """
        path = []
        current = self
        while current is not None:
            path.append((current.state, current.op, current.depth))
            current = current.parent
        path.reverse()
        return path

    # Nodes are compared by f(n), so the priority queue always pops the most
    # promising node first (for BFS/DFS this operator is never used).
    def __lt__(self, other):
        return self.f() < other.f()

    def __str__(self):
        return "state: %s, op: %s, depth: %s, g: %s, h: %s" % (
            self.state, self.op, self.depth, self.cost, self.delta)


class TreeSearch:
    """Search engine for BFS, DFS and A*.

    start       root node (an instance of Node)
    successor   function successor(node) -> list of child Nodes
    goal        function goal(node, goal_state) -> True/False
    strategy    "bfs" (FIFO), "dfs" (LIFO) or "a*" (priority queue)
    goal_state  final node, only needed when the goal test compares states
    heuristic   function heuristic(node, goal_state) -> estimated cost.
                Only used by A*; if omitted h(n)=0 and A* becomes
                Uniform Cost Search (Dijkstra).
    """

    STRATEGIES = ("bfs", "dfs", "a*")

    def __init__(self, start, successor, goal, strategy="bfs",
                 goal_state=None, heuristic=None):
        if strategy not in self.STRATEGIES:
            raise ValueError("unknown strategy %r, use one of %s"
                             % (strategy, list(self.STRATEGIES)))
        self.start = start
        self.successor = successor
        self.goal = goal
        self.strategy = strategy
        self.goal_state = goal_state
        self.heuristic = heuristic
        self.frontier = []   # pending nodes
        self.reached = {}    # state -> best g(n) found so far for that state
        self.iterations = 0  # nodes expanded by the last call to find()

    # ------------------------------------------------------------------
    # Frontier: the only thing that changes between strategies
    # ------------------------------------------------------------------

    def _new_frontier(self):
        """An empty frontier of the right kind for the current strategy."""
        if self.strategy == "bfs":
            return deque()  # FIFO: append right, pop left  -> shallowest first
        return []           # LIFO (dfs) / binary heap (a*)

    def _push(self, n):
        """Add a node to the frontier."""
        if self.strategy == "a*":
            heapq.heappush(self.frontier, n)  # ordered by f(n) = g(n) + h(n)
        else:
            self.frontier.append(n)           # bfs and dfs both append

    def _pop(self):
        """Take the next node out of the frontier."""
        if self.strategy == "a*":
            return heapq.heappop(self.frontier)  # smallest f(n)
        if self.strategy == "bfs":
            return self.frontier.popleft()       # oldest node  -> FIFO
        return self.frontier.pop()               # newest node  -> LIFO

    # ------------------------------------------------------------------
    # Repeated states
    # ------------------------------------------------------------------

    def _keep(self, child):
        """Should this child be added to the frontier?

        BFS/DFS: a state is explored only once, so any state we have already
                 seen is discarded.
        A*:      a state seen before is kept if we have just reached it with a
                 cheaper g(n). Closing a state the first time we generate it
                 (the old behaviour) can discard the optimal path and breaks
                 A*'s optimality.
        """
        previous_cost = self.reached.get(child.state)
        if previous_cost is None:
            return True
        return self.strategy == "a*" and child.cost < previous_cost

    def _expand(self, current):
        """Generate the children of current and push the useful ones."""
        for child in self.successor(current):
            # g(n) = g(parent) + cost of the move that created the child
            child.cost = current.cost + child.step_cost
            if self.strategy == "a*" and self.heuristic is not None:
                child.delta = self.heuristic(child, self.goal_state)
            if self._keep(child):
                self.reached[child.state] = child.cost
                self._push(child)

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def find(self, max_iter=1000000, debug=False):
        """Run the search and return the goal node, or None if it fails.

        The goal test is done when a node is *popped*, not when it is
        generated: with A* that is what guarantees that the first solution
        taken out of the frontier is the cheapest one.
        """
        self.frontier = self._new_frontier()
        self.reached = {self.start.state: self.start.cost}
        self.iterations = 0
        self._push(self.start)

        while self.frontier and self.iterations < max_iter:
            current = self._pop()

            # Lazy deletion: with A* the same state may sit in the heap more
            # than once; the stale (more expensive) copies are ignored.
            if current.cost > self.reached.get(current.state, current.cost):
                continue

            if self.goal(current, self.goal_state):
                if debug:
                    print("goal found after %s expansions" % self.iterations)
                return current

            self.iterations += 1
            self._expand(current)

            if debug and self.iterations % 1000 == 0:
                print("expansion: %s, g: %s, h: %s, f: %s"
                      % (self.iterations, current.cost, current.delta,
                         current.f()))
                print(current.state)

        # Frontier exhausted or iteration limit reached
        if debug:
            print("solution not found after %s expansions" % self.iterations)
        return None


# Backwards compatible names used by the notebooks
node = Node
BlindSearch = TreeSearch
