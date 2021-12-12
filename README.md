<h2>Information</h2>
An SQL command line interface by Squar3 (MySQL only atm)<br>

<h2>WARNINGS</h2>

**This tool is not protected against SQL-Injections!<br>
Please be aware. only for adminstrators usage ^^**

<h2>Pre-requirements</h2>

MySQL <br>
python *[> 3.x]* <br>
python-pip

+ For debian Make sure you have these packages installed: 
```
  sudo apt-get install default-libmysqlclient-dev build-essential python3-dev
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
TODO Simplify selection in EDIT && DELETE<br>
TODO Test the backup on linux/windows/mac<br>
HOLD Fix common errors from py (packages not installed, etc..)<br>
HOLD Finish describe<br>
HOLD Better defense against self-sql-injection<br>
</h6>
