import numpy as np


# --------------------------------------------------------------------------------
# communication with api
# --------------------------------------------------------------------------------
def extract_pairs(pairs):
    """Receives a list of pairs and returns two lists.
    
    Parameters
    ----------
    pairs: list
        List of list.  It mus have shape (N,2).

    Returns
    -------
    x: list
        List of length N with the first set of elements from pairs.

    y: list
        List of length N with the second set of elements from pairs.
    """
    pairs = np.array(pairs)
    if(pairs.shape[1] == 2):
        x = list( pairs[:,0] )
        y = list( pairs[:,1] )
    else:
        raise ValueError(f'Input has dimensions {pairs.shape}, but must be (?,2)')

    return x, y


def list_to_string(values):
    """Format  a list of values into a single string separated by commas

    Parameters
    ----------
    values: list
        List of strings

    Returns
    -------
    values_str: str
        String with the values of the given list separated by commas.
    """
    if(type(values) == str):
        values_str = values
    elif(type(values) in [list, np.ndarray]):
        values_str = ','.join(values)
    else:
        raise ValueError(f'input must be either str or list.  Instead received {type(values)}')

    return values_str