def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True
