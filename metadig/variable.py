"""Functions to manipulate python variables

The functions in variable.py are used to inspect, filter and convert Python
objects.
"""

import sys
import re

from java.util import ArrayList
from java.math import BigDecimal

# CHeck if an object is blank or undefined.
def isBlank(object):

  pattern = re.compile(r'\s+')
  # Depending on the values extracted from the xpath, the following types may be returned
  # by the Java Based scripting engine (jython):
  # - an int (single value, all numeric)
  # - a string
  # - a boolean (i.e. "Yes", "Y", "No", "No") - this type isn't expected for award
  # - a java.util.ArrayList (multiple values, each typed as int, boolean or string)
  if(isinstance(object, int) or isinstance(object, float) or isinstance(object, int)):
      return False
  elif (isinstance(object, str) or isinstance(object, str)):
    # If award is a string, check that it is not all whitespace
    objStripped = re.sub(pattern, '', object)
    if (len(objStripped) == 0):
        return True 
    else:
        return False
  elif(isinstance(object, ArrayList)):
    # Multiple objects exist
    # Return as soon as a non-blank object is found
    # Also, check if all values are blank
    blankFound = False
    for i in range(0, len(object)):
      thisObj = object.get(i)
      if (isinstance(thisObj, int)):
          return False
      else:
        objStripped = re.sub(pattern, '', thisObj)
        if (len(objStripped) == 0):
            blankFound = True
        else:
            return False 
  elif(isinstance(object, list)):
    # Multiple objects exist
    # Return as soon as a non-blank object is found
    # Also, check if all values are blank
    blankFound = False
    for i in range(0, len(object)):
      thisObj = object[i]
      if (isinstance(thisObj, int)):
        return False
      else:
        objStripped = re.sub(pattern, '', thisObj)
        if (len(objStripped) == 0):
          blankFound = True
        else:
          return False 
  
    # If we reached this point and blankFound is true, then all
    # values are blank
    if blankFound: 
        return True
  else:
    raise Exception('Unknown variable type {}'.format(type(object)))
    
def toUnicode(object, *argv):
    """Convert jython and Python types to unicode

    The input object can be either a Jython variable type or a Python variable
    type. The object is converted to a Python unicode object. When ArrayLists and 
    lists are evaluated, each element is inspected and converted to unicode.
    Convertering all variables to unicode, ensures that the quality check code has less 
    checking that it has to do, and also to remove any reference to jython objects in the
    check code (in the future, a pure Python scripting engine may be used).

    Args:
        object (Jython ArrayList or most Python type): the object to be converted
        encoding (str): the encoding scheme to be used, default: "utf-8"

    Returns:
        unicode: either a scalar or list is returned, depending on the input
    """
        
    if(len(argv) > 0):
        encoding = argv[0]
    else:
        encoding = "utf-8"
        
    if(isinstance(object, int)):
        return(str(str(object), encoding))
    elif(isinstance(object, float)):
        return(str(str(object), encoding))
    elif(isinstance(object, int)):
        return(str(str(object), encoding))
    elif(isinstance(object, bool)):
        return(str(str(object), encoding))
    elif (isinstance(object, str)): 
        return(str(object, encoding))
    elif(isinstance(object, list)):
        row = []
        # Multiple objects exist
        # Return as soon as a non-blank object is found
        # Also, check if all values are blank
        for i in range(0, len(object)):
            row.append(toUnicode(object[i], encoding))
        return(row)
    elif(isinstance(object, ArrayList)):
        row = []
        # Multiple objects exist
        # Return as soon as a non-blank object is found
        # Also, check if all values are blank
        for i in range(0, len(object)):
            row.append(toUnicode(object.get(i), encoding))
        return(row)
    elif(isinstance(object, BigDecimal)):
        return(str(object.toString()))
    elif(object is None):
        return object
    else:
        raise Exception('Unknown variable type {}'.format(type(object)))
