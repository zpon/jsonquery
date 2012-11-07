jsonquery
=========

Commandline JSON querying

Example
-------
<blockquote>
$ cat example.json | python jsonquery.py -q $.element
{
    "value": 1234,
      "size": 2
}
$ cat example.json | python jsonquery.py -q $..size
2
</blockquote>
