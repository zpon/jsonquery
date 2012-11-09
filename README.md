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
  }
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
