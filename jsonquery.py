# encoding=utf-8
import sys, json, copy;
import numbers;
import argparse;

"""
Parse json data from standard input and allows querying.
Query language is a subset of JSONPath http://goessner.net/articles/JsonPath/

Created by
Søren Juul <zpon.dk [at] gmail.com>

Lincesed under: Apache 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

parser = argparse.ArgumentParser(description='Query a JSON stream')
parser.add_argument('-q', '--query', type=str, help='Query string', const='$..', nargs='?')
parser.add_argument('-f', '--file', type=str, help='Input file')
args = parser.parse_args()



def show_error_and_exit(error):
  print "jsonquery: " + error
  exit(1)

def jiterate(query, object):
  subobject = object
  cquery = copy.copy(query)
	 
  while len(cquery) > 0:
    element = cquery.pop()

    # Wildcard
    if element == "":
      result = []
      r = jiterate(cquery, subobject)
      if r != None:
        return r
      else:
        recursivequery = cquery
        recursivequery.insert(0, element)
        for key in subobject.keys():
          r = jiterate(recursivequery, subobject[key])
          if r != None:
            result.append(r)
        if len(result) == 1:
          return result[0]
        elif len(result) == 0:
          return
        else:
          return result

    # Get element
    else:
      element_name = element
      index = -1
      # If index is set, retrieve it
      if element.endswith(']'):
        element_name = element[:element.find('[')]
        index = int(element[element.find('[')+1:element.find(']')])

      # If wildcard catch all elements
      if element == "*":
        result = []
        for key in subobject.keys():
          subelement = subobject[key]
          result.append(subelement)
        return result

      # Else extract key
      elif element_name in subobject:
        subobject = subobject[element_name]
        if index > -1:
          if type(subobject) == type(list()) and len(subobject) >= index:
            subobject = subobject[index]
          else:
            show_error_and_exit("List not found as expected.\nError part of query: \"" + element + "\"")
      else:
        return
  return subobject

def pretty_print(object, indent_str):
  str_output = ""

  # Handle lists
  if isinstance(object, list):
    str_output += "["
    for idx, element in enumerate(object):
      str_output += "\n" + indent_str + "\t" +  pretty_print(element, indent_str+"\t")
      if idx < len(object)-1:
        str_output += ","
    str_output += "\n" + indent_str + "]"

  # Handle objects
  elif isinstance(object, dict):
    str_output += "{"
    for idx, key in enumerate(object.keys()):
      str_output += "\n" + "\t" + indent_str + "\"" + key + "\": "
      str_output += pretty_print(object[key], indent_str+"\t")
      if idx < len(object.keys())-1:
        str_output += ","
    str_output += "\n" + indent_str + "}"

  # Handle numbers
  elif isinstance(object, numbers.Number):
    str_output += str(object)

  # Handle rest
  else:
    str_output += "\"" + str(object) + "\""
    
  return str_output

# Read in data
buffered = ""
# If file not set, use std.in
if args.file == None:
  while True:
    read = sys.stdin.readline()
    if read:
      buffered += read
    else:
      break
# Else read the file
else:
  try:
    with open(args.file, 'r') as f:
      buffered = f.read()
  except IOError as e:
    show_error_and_exit("Error opening file: \"" + e.__str__() + "\"")

# Parse input to json
try:
  object = json.loads(buffered)
except ValueError as e:
  show_error_and_exit("JSON input parsing error: \"" + e.__str__() + "\"")

# Parse query
if args.query != None and len(args.query) > 0:
  elements = args.query.split('.')
  elements.reverse()
  if elements[len(elements)-1] == "$":
    elements.pop()
  output = jiterate(elements, object)
else:
  output = object

print pretty_print(output, "")
