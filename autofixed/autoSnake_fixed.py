# automoving. Use snake's current position, suggest a move

# LC stands for Line-Column. The strategy of going vertical until correct line, then horizontal until correct column
# analogue: CL is Col-Line, first horizontal then vertical


def LC_move():
    """returns next move in the LC strategy.
    As a string left/right/up/down.
    """
    from snake import get_headcoord
    from meal import get_mealcoord

    xhead, yhead = get_headcoord()
    xmeal, ymeal = get_mealcoord()

    # test

    # This strategy wants to move vertical first
    dy = ymeal - yhead
    if 0 == dy:
        pass
    elif dy > 0:
        return "down"
    else:
        return "up"

    dx = xmeal - xhead
    if 0 == dx:
        raise ValueError("Snake already at meal position")
    elif dx > 0:
        return "right"
    else:
        return "left"


def LC_path_is_free():
    """True if the simple LC path has no occupied spaces"""

    path = []
    from snake import get_headcoord
    from meal import get_mealcoord

    xhead, yhead = get_headcoord()
    xmeal, ymeal = get_mealcoord()

    # vertical first
    dy = ymeal - yhead
    if dy == 0:
        pass
    elif dy > 0:
        for y in range(yhead + 1, ymeal + 1):
            path.append((xhead, y))
    else:
        for y in range(yhead - 1, ymeal - 1, -1):
            path.append((xhead, y))

    # horizontal now
    dx = xmeal - xhead
    if dx == 0:
        pass
    elif dx > 0:
        for x in range(xhead + 1, xmeal + 1):
            path.append((x, ymeal))
    else:
        for x in range(xhead - 1, xmeal - 1, -1):
            path.append((x, ymeal))

    from snake import occupies_tile

    for coords in path:
        if occupies_tile(coords):
            return False

    return True


def CL_move():
    from snake import get_headcoord
    from meal import get_mealcoord

    xhead, yhead = get_headcoord()
    xmeal, ymeal = get_mealcoord()

    # This strategy wants to move horizontal first
    dx = xmeal - xhead
    if dx == 0:
        pass
    elif dx > 0:
        return "right"
    else:
        return "left"

    dy = ymeal - yhead
    if dy == 0:
        raise ValueError("Snake already at meal position")
    elif dy > 0:
        return "down"
    else:
        return "up"


def CL_path_is_free():
    """True if the simple CL path has no occupied spaces"""

    path = []
    from snake import get_headcoord
    from meal import get_mealcoord

    xhead, yhead = get_headcoord()
    xmeal, ymeal = get_mealcoord()

    # horizontal first
    dx = xmeal - xhead
    if dx == 0:
        pass
    elif dx > 0:
        for x in range(xhead + 1, xmeal + 1):
            path.append((x, yhead))
    else:
        for x in range(xhead - 1, xmeal - 1, -1):
            path.append((x, yhead))

    # vertical now
    dy = ymeal - yhead
    if dy == 0:
        pass
    elif dy > 0:
        for y in range(yhead + 1, ymeal + 1):
            path.append((xmeal, y))
    else:
        for y in range(yhead - 1, ymeal - 1, -1):
            path.append((xmeal, y))

    from snake import occupies_tile

    for coords in path:
        if occupies_tile(coords):
            return False

    return True


# TODO detect suicide-move, generate random non-suicide move
