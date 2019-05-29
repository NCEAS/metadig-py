"""Metadig check utilities
"""

import sys
import re

import java.util.ArrayList as ArrayList

def isBlank(object):

  pattern = re.compile(r'\s+')
  # Depending on the values extracted from the xpath, the following types may be returned
  # - an int (single value, all numeric)
  # - a string
  # - a boolean (i.e. "Yes", "Y", "No", "No") - this type isn't expected for award
  # - a java.util.ArrayList (multiple values, each typed as int, boolean or string)
  if(isinstance(object, int)):
      return False
  elif (isinstance(object, str) or isinstance(object, unicode)):
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
    # If we reached this point and blankFound is true, then all
    # values are blank
    if blankFound: 
        return True
  else:
    raise Exception('Unknown variable type {}'.format(type(object)))

