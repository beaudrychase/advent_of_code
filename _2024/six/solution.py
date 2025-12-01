from bisect import bisect_right, insort
from collections import defaultdict
from enum import Enum, auto
from typing import NamedTuple, Optional

from six.utils import input_multiline


class Orientation(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


class Position(NamedTuple):
    x: int
    y: int


class Snapshot(NamedTuple):
    orientation: Orientation
    position: Position


class Guard:
    repre_to_orientation = {
        "^": Orientation.UP,
        ">": Orientation.RIGHT,
        "V": Orientation.DOWN,
        "<": Orientation.LEFT,
    }
    next_orientation = {
        Orientation.UP: Orientation.RIGHT,
        Orientation.RIGHT: Orientation.DOWN,
        Orientation.DOWN: Orientation.LEFT,
        Orientation.LEFT: Orientation.UP,
    }
    side_of_obstacle = {
        Orientation.UP: Position(0, 1),
        Orientation.RIGHT: Position(-1, 0),
        Orientation.DOWN: Position(0, -1),
        Orientation.LEFT: Position(1, 0),
    }


class GridMap:
    x_indexed_obstacles: defaultdict[int, list[Position]]
    y_indexed_obstacles: defaultdict[int, list[Position]]

    guard_orientation: Orientation
    guard_position: Position
    farthest_corner: Position

    obstacles: list[Position]
    snapshots: list[Snapshot]

    found_loops: set[Position]

    def __init__(self, grid: list[list[str]]):
        self.agent = list()
        self.obstacles = list()
        self.snapshots = list()
        self.farthest_corner = Position(len(grid[0]) - 1, len(grid) - 1)
        self.found_loops = set()

        for y, row in enumerate(grid):
            for x, a in enumerate(row):
                self.make_element(Position(x, y), a)

        self.x_indexed_obstacles = defaultdict(list)
        self.y_indexed_obstacles = defaultdict(list)
        for o in self.obstacles:
            self.x_indexed_obstacles[o.x].append(o)
            self.y_indexed_obstacles[o.y].append(o)
        for lst in self.x_indexed_obstacles.values():
            lst.sort(key=lambda o: o.y)
        for lst in self.y_indexed_obstacles.values():
            lst.sort(key=lambda o: o.x)

    def make_element(self, position: Position, character: str):
        match character:
            case "^" | ">" | "<" | "V":
                self.guard_orientation = Guard.repre_to_orientation[character]
                self.guard_position = position
            case "#":
                self.obstacles.append(position)

    def walk_guard(self):

        guard_position = self.guard_position
        guard_orientation = self.guard_orientation

        while guard_position:
            next_position: Optional[Position] = self.go_to_next_obstacle(
                guard_position, guard_orientation
            )
            if next_position is not None:
                self.record_snapshots(guard_orientation, guard_position, next_position)
            else:
                self.record_walk_to_edge(guard_orientation, guard_position)

            guard_position = next_position
            guard_orientation = Guard.next_orientation[guard_orientation]

    def go_to_next_obstacle(self, agent_position, agent_orientation):
        column = self.x_indexed_obstacles[agent_position.x]
        row = self.y_indexed_obstacles[agent_position.y]
        match agent_orientation:
            case Orientation.UP:
                insert_point = (
                    bisect_right(
                        column,
                        agent_position.y,
                        key=lambda l: l.y,
                    )
                    - 1
                )
                if insert_point < 0:
                    return None
                obstacle = column[insert_point]
            case Orientation.RIGHT:
                insert_point = bisect_right(
                    row,
                    agent_position.x,
                    key=lambda l: l.x,
                )
                if insert_point >= len(row):
                    return None
                obstacle = row[insert_point]
            case Orientation.DOWN:
                insert_point = bisect_right(
                    column,
                    agent_position.y,
                    key=lambda l: l.y,
                )
                if insert_point >= len(column):
                    return None
                obstacle = column[insert_point]
            case Orientation.LEFT:
                insert_point = (
                    bisect_right(
                        row,
                        agent_position.x,
                        key=lambda l: l.x,
                    )
                    - 1
                )
                if insert_point < 0:
                    return None
                obstacle = row[insert_point]
        side = Guard.side_of_obstacle[agent_orientation]
        return Position(obstacle.x + side.x, obstacle.y + side.y)

    def record_snapshots(
        self, orientation: Orientation, position: Position, new_position: Position
    ):
        match orientation:
            case Orientation.UP:
                for y in range(new_position.y, position.y + 1):
                    self.snapshots.append(
                        Snapshot(Orientation.UP, Position(position.x, y))
                    )
            case Orientation.RIGHT:
                for x in range(position.x, new_position.x + 1):
                    self.snapshots.append(
                        Snapshot(Orientation.RIGHT, Position(x, position.y))
                    )
            case Orientation.DOWN:
                for y in range(position.y, new_position.y + 1):
                    self.snapshots.append(
                        Snapshot(Orientation.DOWN, Position(position.x, y))
                    )
            case Orientation.LEFT:
                for x in range(new_position.x, position.x + 1):
                    self.snapshots.append(
                        Snapshot(Orientation.LEFT, Position(x, position.y))
                    )

    def record_walk_to_edge(
        self, agent_orientation: Orientation, agent_position: Position
    ):
        match agent_orientation:
            case Orientation.UP | Orientation.LEFT:
                self.record_snapshots(agent_orientation, agent_position, Position(0, 0))
            case Orientation.DOWN | Orientation.RIGHT:
                self.record_snapshots(
                    agent_orientation,
                    agent_position,
                    Position(self.farthest_corner.x, self.farthest_corner.y),
                )

    def find_loops(self):
        self.walk_guard()
        candidates = {p for _, p in self.snapshots if p != self.guard_position}
        for obstacle_position in candidates:

            insort(
                self.y_indexed_obstacles[obstacle_position.y],
                obstacle_position,
                key=lambda p: p.x,
            )
            insort(
                self.x_indexed_obstacles[obstacle_position.x],
                obstacle_position,
                key=lambda p: p.y,
            )
            if self.is_loop():
                self.found_loops.add(obstacle_position)

            self.y_indexed_obstacles[obstacle_position.y].remove(obstacle_position)
            self.x_indexed_obstacles[obstacle_position.x].remove(obstacle_position)

    def is_loop(self) -> bool:
        visited_turning_points: set[Snapshot] = set()
        agent_position = self.guard_position
        agent_orientation = self.guard_orientation
        while agent_position:
            next_orientation = Guard.next_orientation[agent_orientation]

            next_position: Optional[Position] = self.go_to_next_obstacle(
                agent_position, agent_orientation
            )
            if next_position is None:
                return False

            next_snapshot = Snapshot(next_orientation, next_position)
            if next_snapshot in visited_turning_points:
                return True
            visited_turning_points.add(next_snapshot)
            agent_position = next_position
            agent_orientation = next_orientation
        return False


def solution(input_value: str):
    grid = [[c for c in l] for l in input_value.splitlines()]
    map = GridMap(grid)
    map.walk_guard()
    result = {p for _, p in map.snapshots}
    return str(len(result))


def solution_two(input_value: str):
    grid = [[c for c in l] for l in input_value.splitlines()]
    map = GridMap(grid)
    map.find_loops()
    return str(len(map.found_loops))


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
    print(solution_two(input_value))
