from enum import Enum
from os import system
from random import randint, choice, shuffle
from sys import platform
from time import sleep
from types import UnionType
from typing import Optional, Type, Iterator, Self
from colorama import Fore, Style, init

from vec2 import Vec2, vec_scalar_multiply, vec_add, vec_invert


class User:
    def __init__(self) -> None:
        self.board: MainBoard = new_board(SquareState.EMPTY, BOARD_HEIGHT, BOARD_WIDTH)
        self.ships: list[Ship] = []
        self.knowledge: KnowledgeBoard = new_board(
            KnowledgeSquareState.UNKNOWN, BOARD_HEIGHT, BOARD_WIDTH
        )


class Ship:
    def __init__(self, squares: list[Vec2]) -> None:
        self.hits: int = 0
        self.sunk: bool = False
        self.squares: list[Vec2] = squares

    def hit(self) -> bool:
        # Returns True if ship is sunk
        self.hits += 1
        if self.hits == len(self.squares):
            self.sunk = True
            return True
        return False


class Orientation(Enum):
    N = Vec2(0, -1)
    E = Vec2(1, 0)
    S = Vec2(0, 1)
    W = Vec2(-1, 0)


class SquareState(Enum):
    EMPTY = " "
    SHIP = "#"
    MISS = "·"
    HIT = "X"


class KnowledgeSquareState(Enum):
    UNKNOWN = " "
    MISS = "·"
    HIT = "X"


# Constants
LOOP_MAX = 100000
BOARD_WIDTH = 10
BOARD_HEIGHT = 10
SHIP_LENGTHS = [5, 4, 3, 3, 2]
# Types
MainBoard: Type = list[list[SquareState]]
KnowledgeBoard: Type = list[list[KnowledgeSquareState]]
Board: UnionType = MainBoard | KnowledgeBoard


def shuffled(a: list) -> list:
    shuffle(a)
    return a


def clear() -> None:
    if platform == "win32":
        _ = system("cls")
    else:
        _ = system("clear")


def new_board(default, height, width) -> Board:
    return [[default for _ in range(width)] for _ in range(height)]


def square_in_board(square: Vec2, board: Board) -> bool:
    width = len(board[0])
    height = len(board)
    return 0 <= square.x < width and 0 <= square.y < height


def random_square(board: Board, matching: SquareState | KnowledgeSquareState) -> Vec2:
    board_height = len(board)
    board_width = len(board[0])
    for _ in range(LOOP_MAX):
        coord = Vec2(randint(0, board_height - 1), randint(0, board_width - 1))
        if board[coord.y][coord.x] is matching:
            return coord
    exit(200)


def extend(origin: Vec2, direction: Vec2, length: int) -> Vec2:
    return vec_add(origin, vec_scalar_multiply(direction, length))


def new_valid_ship(
    origin: Vec2, orientation: Orientation, length: int, owner: User
) -> Optional[Ship]:
    squares = [extend(origin, orientation.value, i) for i in range(length)]
    # Confirm all squares are in the board
    if not all(square_in_board(square, owner.board) for square in squares):
        return None
    # Check if any already placed ships' squares overlap with our squares
    if any(
        len([square for square in squares if square in existing_ship.squares]) > 0
        for existing_ship in owner.ships
    ):
        return None

    return Ship(squares)


def place_ship(ship: Ship, board: Board) -> None:
    for square in ship.squares:
        board[square.y][square.x] = SquareState.SHIP


class FireResult(Enum):
    HIT = 1
    MISS = 2
    FAIL = 3
    SUNK = 4


def fire_missile(coord: Vec2, source: User, target: User) -> FireResult:
    # If already fired at this square
    if source.knowledge[coord.y][coord.x] != KnowledgeSquareState.UNKNOWN:
        return FireResult.FAIL
    # Check if shot is a hit or a miss
    for ship in target.ships:
        if coord in ship.squares:
            sunk = ship.hit()
            target.board[coord.y][coord.x] = SquareState.HIT
            source.knowledge[coord.y][coord.x] = KnowledgeSquareState.HIT
            return FireResult.SUNK if sunk else FireResult.HIT
    else:
        source.knowledge[coord.y][coord.x] = KnowledgeSquareState.MISS
        target.board[coord.y][coord.x] = SquareState.MISS
        return FireResult.MISS


def display_board(board: Board) -> None:
    height = len(board)
    width = len(board[0])
    print("│   " + " ".join([str(x) for x in range(width)]) + "   │")
    for y in range(height):
        print(f"│ {chr(y + 65)} ", end="")
        print(*[square.value for square in board[y]], sep=" ", end="   │\n")


def display_boards(user: User) -> None:
    clear()
    board_width = len(user.board[0])
    line_width = board_width * 2 + 5
    print("┌" + "─" * line_width + "┐")
    display_board(user.knowledge)
    print("├" + "─" * line_width + "┤")
    display_board(user.board)
    print("└" + "─" * line_width + "┘")


def message(text: str, user: User, colour: str = "") -> None:
    display_boards(user)
    print(colour + text + Style.RESET_ALL)
    sleep(len(text.split(" ")) / 4 + 0.5)


def decode_notation(text: str, board: Board) -> Optional[Vec2]:
    if len(text) != 2:
        return None
    try:
        # "a" = 0
        row = ord(text.lower()[0]) - 97
        column = int(text[1])
        if not square_in_board(Vec2(column, row), board):
            return None
    except ValueError:
        return None

    return Vec2(column, row)


class State:
    def update(self, user: User, player: User) -> Optional[Self]:
        pass


class RandomState(State):
    def update(self, user: User, player: User) -> Optional[State]:
        target = random_square(user.knowledge, KnowledgeSquareState.UNKNOWN)
        result = fire_missile(target, user, player)
        if result == FireResult.HIT:
            return LookAroundState(user, target)


class LookAroundState(State):
    def __init__(self, user: User, centre: Vec2):
        self.centre = centre
        self.to_check: Iterator[Orientation] = (
            orientation
            for orientation in shuffled(list(Orientation))
            if square_in_board(vec_add(centre, orientation.value), user.board)
        )

    def update(self, user: User, player: User) -> Optional[State]:
        try:
            orientation = next(self.to_check)
        except StopIteration:
            return RandomState()
        result = fire_missile(vec_add(self.centre, orientation.value), user, player)
        match result:
            case FireResult.HIT:
                return ExploreState(self.centre, orientation)
            case FireResult.SUNK:
                return RandomState()
            case _:
                # Miss or Fail (shouldn't fail)
                return None


class ExploreState(State):
    def __init__(self, centre: Vec2, orientation: Orientation):
        self.centre = centre
        self.orientation: Orientation = orientation
        self.check_opposite: bool = False
        self.extent = 1

    def update(self, user: User, player: User) -> Optional[State]:
        # Fully explore the orientation
        self.extent += 1
        if self.check_opposite:
            result = fire_missile(
                extend(self.centre, vec_invert(self.orientation.value), self.extent),
                user,
                player,
            )
            match result:
                case FireResult.MISS | FireResult.SUNK:
                    return RandomState()
                case FireResult.FAIL:
                    return self.update(user, player)
                case _:
                    return None

        result = fire_missile(
            extend(self.centre, self.orientation.value, self.extent),
            user,
            player,
        )
        match result:
            case FireResult.MISS:
                self.check_opposite = True
                self.extent = 0
                return None
            case FireResult.FAIL:
                self.check_opposite = True
                self.extent = 0
                return self.update(user, player)
            case FireResult.SUNK:
                return RandomState()
            case _:
                return None


def battleships() -> None:
    # AI ship placement
    ai = User()
    for length in SHIP_LENGTHS:
        new_ship = None
        while new_ship is None:
            new_ship = new_valid_ship(
                random_square(ai.board, SquareState.EMPTY),
                choice(list(Orientation)),
                length,
                ai,
            )
        ai.ships.append(new_ship)
        place_ship(new_ship, ai.board)

    # Player ship placement
    player = User()
    available_ship_lengths = SHIP_LENGTHS
    boards = [player.knowledge, player.board]
    while len(available_ship_lengths) > 0:
        display_boards(player)

        inp = input("Enter start/end points of a ship to place it (e.g. c0 c2): ")
        if inp == "exit":
            return
        point_a, point_b = (decode_notation(w, player.board) for w in inp.split(" "))
        if point_a is None or point_b is None:
            message("Error: One or more points invalid", player)
            continue

        if point_a.y == point_b.y:
            displacement = point_b.x - point_a.x
            orientation = Orientation.E if displacement > 0 else Orientation.W
        elif point_a.x == point_b.x:
            displacement = point_b.y - point_a.y
            orientation = Orientation.S if displacement > 0 else Orientation.N
        else:
            # Diagonal
            continue

        length = abs(displacement) + 1
        if length in available_ship_lengths:
            new_ship = new_valid_ship(point_a, orientation, length, player)
            if new_ship is not None:
                available_ship_lengths.remove(length)
                player.ships.append(new_ship)
                place_ship(new_ship, player.board)
        else:
            message("Error: Ship length not available", player)

    # Main game loop
    ai_state: State = RandomState()
    while True:
        # Player turn
        result = FireResult.FAIL
        while result == FireResult.FAIL:
            display_boards(player)
            inp = input("Enter square to fire missile (e.g. c4): ")
            square = decode_notation(inp, player.board)
            if square is None:
                message("Error: invalid square", player, colour=Fore.RED)
                continue
            result = fire_missile(square, player, ai)
            match result:
                case FireResult.SUNK:
                    message("Enemy: You sunk my battleship!", player, colour=Fore.GREEN)
                case FireResult.MISS:
                    message("Enemy: Miss!", player, colour=Fore.BLUE)
                case FireResult.HIT:
                    message("Enemy: Hit...", player, colour=Fore.GREEN)
                case FireResult.FAIL:
                    message("Error: Already fired there.", player, colour=Fore.RED)

        # AI turn
        state = ai_state.update(ai, player)
        if state is not None:
            ai_state = state

        # Win condition
        if all(ship.sunk for ship in player.ships):
            display_boards(*boards)
            input("You LOST! Press enter...")
            break
        if all(ship.sunk for ship in ai.ships):
            display_boards(*boards)
            input("You WON! Press enter...")
            break


init()

if __name__ == "__main__":
    while True:
        battleships()
