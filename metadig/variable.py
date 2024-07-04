"""Functions to manipulate python variables

The functions in variable.py are used to inspect, filter and convert Python
objs.
"""

import re

try:
    from java.util import ArrayList
    from java.math import BigDecimal
except ImportError:
    pass


# Check if an object is blank or undefined.
def isBlank(obj):

    pattern = re.compile(r"\s+")
    # Depending on the values extracted from the xpath, the following types may be returned
    # by the Java Based scripting engine (jython):
    # - an int (single value, all numeric)
    # - a string
    # - a boolean (i.e. "Yes", "Y", "No", "No") - this type isn't expected for award
    # - a java.util.ArrayList (multiple values, each typed as int, boolean or string)
    if isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, int):
        return False
    elif isinstance(obj, str):
        # If award is a string, check that it is not all whitespace
        objStripped = re.sub(pattern, "", obj)
        if len(objStripped) == 0:
            return True
        else:
            return False
    elif isinstance(obj, ArrayList):
        # Multiple objects exist
        # Return as soon as a non-blank object is found
        # Also, check if all values are blank
        blankFound = False
        for i in range(0, len(obj)):
            thisObj = obj.get(i)
            if isinstance(thisObj, int):
                return False
            else:
                objStripped = re.sub(pattern, "", thisObj)
                if len(objStripped) == 0:
                    blankFound = True
                else:
                    return False
    elif isinstance(obj, list):
        # Multiple objects exist
        # Return as soon as a non-blank object is found
        # Also, check if all values are blank
        blankFound = False
        for i in range(0, len(obj)):
            thisObj = obj[i]
            if isinstance(thisObj, int):
                return False
            else:
                objStripped = re.sub(pattern, "", thisObj)
                if len(objStripped) == 0:
                    blankFound = True
                else:
                    return False

        # If we reached this point and blankFound is true, then all
        # values are blank
        if blankFound:
            return True
    else:
        raise Exception("Unknown variable type {}".format(type(obj)))


def toUnicode(obj, *argv):
    """Convert jython and Python types to unicode

    The input obj can be either a Jython variable type or a Python variable
    type. The obj is converted to a Python unicode obj. When ArrayLists and
    lists are evaluated, each element is inspected and converted to unicode.
    Convertering all variables to unicode, ensures that the quality check code has less
    checking that it has to do, and also to remove any reference to jython objs in the
    check code (in the future, a pure Python scripting engine may be used).

    Args:
        obj (Jython ArrayList or most Python type): the obj to be converted
        encoding (str): the encoding scheme to be used, default: "utf-8"

    Returns:
        unicode: either a scalar or list is returned, depending on the input
    """

    if len(argv) > 0:
        encoding = argv[0]
    else:
        encoding = "utf-8"

    if isinstance(obj, int):
        return str(str(obj), encoding)
    elif isinstance(obj, float):
        return str(str(obj), encoding)
    elif isinstance(obj, int):
        return str(str(obj), encoding)
    elif isinstance(obj, bool):
        return str(str(obj), encoding)
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, list):
        row = []
        # Multiple objs exist
        # Return as soon as a non-blank obj is found
        # Also, check if all values are blank
        for i in range(0, len(obj)):
            row.append(toUnicode(obj[i], encoding))
        return row
    elif isinstance(obj, ArrayList):
        row = []
        # Multiple objs exist
        # Return as soon as a non-blank obj is found
        # Also, check if all values are blank
        for i in range(0, len(obj)):
            row.append(toUnicode(obj.get(i), encoding))
        return row
    elif isinstance(obj, BigDecimal):
        return str(obj.toString())
    elif obj is None:
        return obj
    else:
        raise Exception("Unknown variable type {}".format(type(obj)))
