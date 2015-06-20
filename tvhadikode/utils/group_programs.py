# -*- encoding: utf-8 -*-

def group_programs(programs):
    """
    Groups a list of programs by start date.

    >>> [Program(), Program(), ...]

    becomes

    >>> [(DateTime(), [Program(), Program(), ...]),
    >>>  (DateTime(), [Program(), Program(), ...], ...]

    This function implied that programs is ordered by start in ascending order!
    """
    result = []
    current_date = None

    for program in programs:
        if current_date != program.start.date():
            result.append((program.start.date(), []))
            current_date = program.start.date()
        result[-1][1].append(program)
    return result
