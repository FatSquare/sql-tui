<h2>Information</h2>
An SQL command line interface by Squar3 (MySQL only atm)<br>


<h2>WARNINGS</h2>

This tool is not anywhere close to finish!<br> 
  
<h2>Pre-requirements</h2>

**Dependecis**

MySQL <br>
python3 <br>
python3-pip

+ For debian Make sure you have these packages installed (after installing mysql): 
```
  sudo apt-get install default-libmysqlclient-dev build-essential python3-dev python3-pip python3
```

<h2>Installation</h2>

**Linux** 

``` bash
git clone https://github.com/FatSquare/sql-cli.git && cd sql-cli/ && pip install -r requirements.txt
python sql-cli.py
```



<hr>

<h4>Todo List</h4>

<h6>
TODO Simplify selection in DELETE (checkbox like EDIT) <br>
TODO check for self-sql-injections in user input  <br>
</h6>
