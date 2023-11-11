from battleships import *


class AIState:
    def update(self, ai: User, player: User) -> Optional[Self]:
        pass


class RandomState(AIState):
    def update(self, ai: User, player: User) -> Optional[AIState]:
        target = random_square(ai.knowledge, KnowledgeSquareState.UNKNOWN)
        result = fire_missile(target, ai, player)
        if result == FireResult.HIT:
            return ExploreState(ai, target)


class ExploreState(AIState):
    def __init__(self, ai: User, centre: Vec2):
        self.centre = centre
        self.to_check: Iterator[Orientation] = (
            orientation
            for orientation in list(Orientation)
            if square_in_board(vec_add(centre, orientation.value), ai.board)
        )
        self.found_orientation: Optional[Orientation] = None
        self.check_opposite: bool = False
        self.extent = 1

    def update(self, ai: User, player: User) -> Optional[AIState]:
        if self.found_orientation is None:
            # Look around
            try:
                orientation = next(self.to_check)
                result = fire_missile(
                    vec_add(self.centre, orientation.value), ai, player
                )
                if result == FireResult.HIT:
                    self.found_orientation = orientation
                elif result == FireResult.SUNK:
                    return RandomState()
                else:
                    # Miss or Fail
                    return None
            except StopIteration:
                return RandomState()
        else:
            # Fully explore the orientation
            self.extent += 1
            if self.check_opposite:
                orientation = self.found_orientation
                result = fire_missile(
                    extend(self.centre, vec_invert(orientation.value), self.extent),
                    ai,
                    player,
                )
                match result:
                    case FireResult.MISS | FireResult.SUNK:
                        return RandomState()
                    case FireResult.FAIL:
                        return self.update(ai, player)
                    case _:
                        return None
            else:
                orientation = self.found_orientation
                result = fire_missile(
                    extend(self.centre, orientation.value, self.extent),
                    ai,
                    player,
                )
                match result:
                    case FireResult.MISS | FireResult.FAIL:
                        self.check_opposite = True
                        self.extent = 0
                        if result == FireResult.FAIL:
                            return self.update(ai, player)
                        else:
                            return None
                    case FireResult.SUNK:
                        return RandomState()
                    case _:
                        return None
