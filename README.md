jsonquery
=========

Commandline JSON querying

Example
-------
example.json:
```
{
  "element" : {
    "value" : 1234,
    "size" : 2
  },
  "array" : [
    123,
    456,
    789
  ]
}
```

Get the *element* object
```
$ cat example.json | python jsonquery.py -q $.element
{
    "value": 1234,
    "size": 2
}
```
Look in all objects for the *size* element
```
$ cat example.json | python jsonquery.py -q $..size
2
```
Take output from first example and select *size* element from that
```
$ cat example.json | python jsonquery.py -q $.element | python jsonquery.py -q $.size
2
```
Find all elements in JSON object
```
python jsonquery.py -f examples/example.json -q $..*
[
    [
        123,
        456,
        789
    ],
    {
        "value": 1234,
        "size": 2
    }
]
```
Find extract second element in array
```
$ python jsonquery.py -f examples/example.json -q $.array[1]
456
```

Resources
---------
* Online JSONPath Expression Tester: http://jsonpath.curiousconcept.com/
* Description of JSONPath: http://goessner.net/articles/JsonPath/
