import numpy as np

from datetime import datetime, timedelta


# --------------------------------------------------------------------------------
# functions
# --------------------------------------------------------------------------------
def dates_arange(ti, tf=None, dt=None):
    """Create an array of datetime objects.

    Parameters
    ----------
    ti: datetime.datetime
        Starting date.

    tf: datetime.datetime, optional
        Final date.  Default: datetime.today()

    dt: datetime.timedelta, optional
        spacing between array elements.  Default: datetime.timedelta(days=1)

    Returns
    -------
    dates: list
        List of datetime.datetime objects.
    """
    if(tf is None):
        tf = datetime.today()
    if(dt is None):
        dt = timedelta(days=1)
    
    dates = np.arange(ti, tf, dt).astype(datetime)
    
    return dates


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