from typing import Union, Tuple, List

Direction = Union[Tuple[int, int], List[int]]

from location import Location
import constants as c


def ray_from(start: Location, direction: Direction) -> List[Location]:
    """Create ray starting at a given location, going outwards in a given direction"""
    if direction[0] == 0 and direction[1] == 0:
        raise ValueError("Direction iterable cannot only contain 0's.")
    ray = []
    file_dir = direction[0]
    rank_dir = direction[1]

    stationary = True if (file_dir == 0 or rank_dir == 0) else False

    if not stationary:  # diagonal move.
        file_end, file_step = (9, 1) if file_dir > 0 else (0, -1)
        rank_end, rank_step = (9, 1) if rank_dir > 0 else (0, -1)
        rank_range = range(start.rank, rank_end, rank_step)
        file_range = range(start.file.value, file_end, file_step)
        for file, rank in zip(file_range, rank_range):
            loc = Location(c.Files(file), rank)
            ray.append(loc)

    else:  # Horizontal or vertical move
        if file_dir == 0:
            end, step = (9, 1) if rank_dir > 0 else (0, -1)
            rank_increments = range(start.rank, end, step)
            for rank in rank_increments:
                loc = Location(start.file, rank)
                ray.append(loc)
        else:
            end, step = (9, 1) if file_dir > 0 else (0, -1)
            file_increments = range(start.file.value, end, step)
            for file in file_increments:
                loc = Location(c.Files(file), start.rank)
                ray.append(loc)

    return ray


start = Location(c.Files.D, 3)
ray = ray_from(start, (1, -1))
print(ray_from)

# acts as a predicate... returns Bool based on some condiitons
def is_palendrome(num):
    if num // 10 == 0:
        return False
    temp = num
    reversed_num = 0

    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    if num == reversed_num:
        return True
    else:
        return False


# Our generator that continuously yields a number IF it is a palendrome
# i is a number that is first sent out of the generator.
# When it's sent, the process STOPS.
# We're using send, to change the value of i. we sent the number to the value of i
# and increment it up by 1 and keep going.
def infinite_palendromes():
    num = 0
    while True:
        if is_palendrome(num):
            i = yield num
            if i is not None:
                num = i

        num += 1


# This is the driving code.
# We create the generator.
# We iterate through the generator. For each number the gen gives us, we take
# it's digit length and if it's equal 10, we close the generator.
# If not, we then send back a new value to the generator. (10^digits.)

# pal_gen = infinite_palendromes()
# for i in pal_gen:
#     print(i)
#     digits = len(str(i))
#     if digits == 10:
#         pal_gen.close()
#     pal_gen.send(10 ** digits)
