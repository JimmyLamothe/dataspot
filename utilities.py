""" Simple functions that don't interface with the Spotify API """

def combine_unique(list_1, list_2):
    """ Combine two lists in order whithout duplicates | list, list --> list """
    for item in list_2:
        if not item in list_1:
            list_1.append(item)
    return list_1

