Requiremnet
-----------
python33, recommmend version 3.7

How to split file
--------------------
```bash
python33 fileiter.py -f FILENAME -n NUMBER_OF_SPLITS
```

Create new example file. See example.py as a template. 

How to run MapReduce
--------------------
execute following commands
```bash
python3 example.py
python3 distmm.py -v -n 2
```
The system will spawn two clients and write logs to file mptest.log

For more command-line options
```bash
python3 distmm.py -h
```

How to test
--------------------
```bash
python33 -m unittest discover -v
```