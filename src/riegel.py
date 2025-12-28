def riegel(t1, d1, d2):
    if d1 == 0:
        raise ValueError("d1 must be > 0")
    return t1 * (d2 / d1) ** 1.06