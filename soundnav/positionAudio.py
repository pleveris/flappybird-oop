"""
Implementation of basic audio volume, panning, distancing between points, moving points from one coordinate to another
Sudo 3d audio.
"""

import math
from typing import Tuple, Union


def distance(
    listener: Tuple[Union[int, float], Union[int, float]],
    target: Tuple[Union[int, float], Union[int, float]],
) -> float:
    """
    Calculates 2d distance between 2 points in cartesian system.
    If result is 0 then points are exactly in the same place.

    :param listener: (x, y) of listener
    :type listener: Tuple[int, int] or Tuple[float, float]
    :param target: (x, y) of the sound away from listener
    :type target: Tuple[int, int] or Tuple[float, float]
    :return: Straight distance between 2 points
    :retrtype: float
    """

    # Lengths of the coordinates powered of 2
    deltaX: float = (target[0] - listener[0]) ** 2
    deltaY: float = (target[1] - listener[1]) ** 2

    # Calculate straight distance
    return math.sqrt(deltaX + deltaY)


def absoluteDirection(
    listener: Tuple[Union[int, float], Union[int, float]],
    target: Tuple[Union[int, float], Union[int, float]],
) -> float:
    """
    Calculates angle in radians between listener and target from the listener's perspective (absolute - east = 0deg, north = 90deg - counterclockwise).

    :param listener: (x, y) of listener
    :type listener: Tuple[int, int] or Tuple[float, float]
    :param target: (x, y) of audio target
    :type target: Tuple[int, int] or Tuple[float, float]
    :return: Angle between 2 points in degrees
    :retrtype: float
    """

    assert (
        listener[0] >= 0 and listener[1] >= 0 and target[0] >= 0 and target[1] >= 0
    ), "X and Y must be positive or equal to 0 for both sources."

    # Lengths
    deltaX: float = target[0] - listener[0]
    deltaY: float = target[1] - listener[1]

    # Arctangent of the given lengths determine the angle in radians
    # atan2 takes care of quadrants and illegal devision from 0 for us
    theta: float = math.atan2(deltaY, deltaX)

    assert (
        theta >= 0 and theta <= math.pi * 2
    ), "Calculated theta must be in range 0...2pi"

    return math.degrees(theta)


def move(
    point: Tuple[Union[int, float], Union[int, float]],
    direction: float,
    distance: float = 1.0,
) -> Tuple[float, float]:
    """
    Calculates new cartesian coordinates after movement from given coordinates in given distance and direction.
    This correctly works in upper right quadrant so coordinates should be positive.

    :param point: (x, y) point from which movement should occur
    :type point: Tuple[int, int] or Tuple[float, float]
    :param float direction: Direction in degrees (0...360) in which point should travel
    :param float distance: Distance in units how long point should travel (1.0 = move per 1 coordinate if movement is straight)
    :return: New coordinates (x, y) on which point would be after traveling to the given direction by given distance
    :retrtype: Tuple[float, float]
    """

    assert point[0] >= 0, "Coordinate x must be positive or equal to 0"
    assert point[1] >= 0, "Coordinate y must be positive or equal to 0"
    assert direction >= 0 and direction <= 360, "Direction must be in range 0...360"
    assert distance >= 0, "Distance can not be negative"

    # Cos represents x
    # Cos = adjacent / hypotenuse
    x: float = point[0] + distance * math.cos(math.radians(direction))
    # Sin represents y
    # Sin = opposite / hypotenuse
    y: float = point[1] + distance * math.sin(math.radians(direction))

    # Make sure that neither x or y go out of top right quadrant
    if x < 0 or y < 0:
        raise ValueError("After movement X or Y is < 0. (X; Y): (", x, " ;", y, ").")

    return (x, y)


def _angle(
    listener: Tuple[float, float], target: Tuple[float, float], facingDirection: float
) -> float:
    """
    Returns fixed listener's facing direction, acording to the quadrant and both listener and target positions on the cartesian (angle is in radians).
    This method is for internal usage.
    """

    dist = distance(listener, target)
    if dist == 0:
        return 0.0

    aCos = math.acos((target[0] - listener[0]) / dist)

    if target[1] - listener[1] > 0:
        a = aCos
    else:
        a = -aCos

    return a - math.radians(facingDirection)


def pan(
    listener: Tuple[float, float], target: Tuple[float, float], facingDirection: float
) -> Tuple[float, float]:
    """
    Returns tuple of (left, right) speakers balanced volumes based on listener's facing direction and both listener and target positions.
    """
    angle = _angle(listener, target, facingDirection)
    dist = distance(listener, target)

    # Vertical component
    leftSpeaker = (math.sin(angle) + 1) / 2.0

    # Make it to pan to the right by subtracting left channel's volume from right channel
    rightSpeaker = 1.0 - leftSpeaker
    # Adapt it to be based on 90 degree panning and avoid negative volume steps
    rightSpeaker = math.sin(rightSpeaker * math.pi / 2.0)

    # Check if sound is behind the listener
    if math.cos(angle) < 0:  # Since behind, just reduce the volume to imitate that
        leftSpeaker /= 2.0
        rightSpeaker /= 2.0

    if dist < 1:
        dist = 1.0

    leftSpeaker = min(leftSpeaker / dist, 1.0)
    rightSpeaker = min(rightSpeaker / dist, 1.0)

    return (leftSpeaker, rightSpeaker)


def calcVolume(
    listener: Tuple[float, float],
    target: Tuple[float, float],
    facingDirection: float = 0,
    maxHearingDistance: float = 50.0,
) -> Tuple[float, float]:
    """
    Makes all the real job - calculates balance / panning, adapts volume by maximum distance and returns tuple to be used with Pygame library as volume.
    """

    # Volume by max hearing distance (applying volume per step)
    vol = round(1.0 - (1.0 / maxHearingDistance * distance(listener, target)), 2)
    if vol <= 0:
        return (0.0, 0.0)

    x = listener[0] / vol
    y = listener[1] / vol

    return pan((x, y), target, facingDirection)
