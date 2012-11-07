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
parser.add_argument('-q', '--query', type=str, help='Query string', const='*', nargs='?')
args = parser.parse_args()

buffered = ""
while True:
  read = sys.stdin.readline()
  if read:
    buffered += read
  else:
    break

object = json.loads(buffered)

def show_error_and_exit(error):
  print "ERROR : " + error
  exit(1)

def jiterate(query, object):
  subobject = object
	 
  while len(query) > 0:
    element = query.pop()

    # Wildcard
    if element == "":
      result = []
      for key in subobject.keys():
        r = jiterate(query, subobject[key])
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
      if element.endswith(']'):
        element_name = element[:element.find('[')]
        index = int(element[element.find('[')+1:element.find(']')])
      if element_name in subobject:
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

if args.query != None and len(args.query) > 0:
  elements = args.query.split('.')
  elements.reverse()
  if elements[len(elements)-1] == "$":
    elements.pop()
  output = jiterate(elements, object)
else:
  output = object
print pretty_print(output, "")
