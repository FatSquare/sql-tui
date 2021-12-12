#! /usr/bin/env python
from prettytable import PrettyTable 
from sqlalchemy import*
from sqlalchemy.sql import text
from config import*
from colorama import Fore
import time,os,inspect
from datetime import datetime 

def printf(msg,color=Fore.WHITE):
    print(color + msg + Fore.WHITE)

def clear(force=False):
    if allow_clear_console==True or force==True:
        if os.name == 'nt':os.system('cls')
        else: os.system('clear') 
    else:
        print('\n')
clear(True)

#Sql injection warning
if sqli_warning==True: 
    printf("THIS PRODUCS SHOULD BE AVALIABLE ONLY FOR ADMINSTARTORS, IT IS NOT PROTECTED AGAINST SQL INJECTIONS!",Fore.RED)
    printf("Sql-cli will start in 5 seconds..",Fore.YELLOW)
    printf("if you want to stop this please set sqli_warning to False in config.py",Fore.YELLOW)
    time.sleep(5)
    printf("Trying to connect to database using config.py",Fore.YELLOW)

#Setup
engine = create_engine('mysql+pymysql://'+username+':'+password+'@'+host+'/'+database)
conn=False
metadata=0

#Startup
print("Author: Squar3")
print("Github: https://github.com/FatSquare/sql-cli/sql-cli.git");
print("""
 ____        _            _ _ 
/ ___|  __ _| |       ___| (_)
\___ \ / _` | |_____ / __| | |
 ___) | (_| | |_____| (__| | |
|____/ \__, |_|      \___|_|_|
          |_|                 
""")

#Database connection
printf("Connecting to database",Fore.YELLOW)
try:
    conn = engine.connect()
    metadata = MetaData()
    printf("Connected successfully!",Fore.GREEN)
except:
    exit(printf("Error while conncting to database..",Fore.RED))
time.sleep(1)

#Program
def Home(inc=0):
    clear()
    if(inc==1):printf("Incorrect option: ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    printf("SELECT OPTION:",Fore.CYAN)
    printf("[1] VIEW    :",Fore.LIGHTGREEN_EX)
    printf("[2] INSERT  :",Fore.LIGHTGREEN_EX)
    printf("[3] EDIT    :",Fore.LIGHTGREEN_EX)
    printf("[4] DELETE  :",Fore.LIGHTGREEN_EX)
    printf("[5] DESCRIBE:",Fore.YELLOW)
    printf("[6] BACKUP  :",Fore.LIGHTGREEN_EX)
    printf("[7] EXIT    :",Fore.LIGHTGREEN_EX)
    r = input(Fore.LIGHTGREEN_EX + "OPTION: " + Fore.WHITE).replace('[','').replace(']','')
    if   r=='1':VIEW()
    elif r=='2':INSERT()
    elif r=='3':EDIT()
    elif r=='4':DELETE()
    elif r=='5':DESCRIBE()
    elif r=='6':BACKUP()
    elif r=='7':exit()
    else:Home(1)

def VIEW(inc=0):
    clear()
    if(inc==1):printf("Incorrect table name! ",Fore.RED)
    if(inc==2):printf("Incorrect columns name! ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    printf("SELECT OPTION:",Fore.CYAN)
    #list all tables
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables = PrettyTable(["TABLES"])
    for i in conn.execute(query):tables.add_row(i)
    print(tables)
    r = input(Fore.LIGHTGREEN_EX + "TABLE NAME: " + Fore.WHITE)
    d=""
    cls=[]
    try:
        d = Table(r, metadata, autoload=True, autoload_with=engine)
        cls=d.columns.keys()
        printf(str(cls),Fore.GREEN)
    except:
        VIEW(1)
    print(Fore.LIGHTGREEN_EX+"Columns -> "+Fore.YELLOW +"DEFAULT("+",".join(cls)+")"+Fore.WHITE)
    b = input(Fore.LIGHTGREEN_EX+"Columns: "+Fore.WHITE)
    if b=="":b=",".join(cls) # ALL COLUMNS
    query = text(f"SELECT {b} FROM {r};")
    try:
        rs = conn.execute(query)
    except:
        VIEW(2)
    print(b.split(','))
    myTable = PrettyTable(b.split(','))
    for row in rs:
        myTable.add_row(row)
    print(myTable)
    input("PRESS ANY KEY TO GO BACK HOME!")
    Home()

def INSERT(inc=0):
    clear() 
    if(inc==1):printf("Incorrect table name! ",Fore.RED)
    if(inc==2):printf("COLUMN HAS NO DEFAULT VALUE ! ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    printf("SELECT OPTION:",Fore.CYAN)
    r = input(Fore.LIGHTGREEN_EX + "TABLE NAME: " + Fore.WHITE)
    d=""
    cls=[]
    try:
        d = Table(r, metadata, autoload=True, autoload_with=engine)
        cls=d.columns.keys()
        printf(str(cls),Fore.GREEN)
    except:
        INSERT(1)
    cols = ""
    data = ""
    printf("Press \"ENTER\" for default!")

    for cl in cls:
        CL = input(cl+": ")
        if CL != "":
            data += '"' + CL.replace('"','\"') + '"' + ',' #Common self-defense sqli (NOT SECURE AT ALL)
            cols += cl + ',' 
    
    data=data[:-1];cols=cols[:-1]
    query = f'INSERT INTO {r}({cols}) VALUES({data})'

    try:
        rs = conn.execute(query)
        printf("DATA INSERTED SUCCESSFULLY",Fore.GREEN)
    except:
        INSERT(2)

    input("PRESS ANY KEY TO GO BACK HOME!")
    Home()

def EDIT(inc=0):
    clear() 
    if(inc==1):printf("Incorrect table  name! ",Fore.RED)
    if(inc==2):printf("Incorrect column name! ",Fore.RED)
    if(inc==3):printf("Incorrect condition! ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    printf("SELECT OPTION:",Fore.CYAN)
    r = input(Fore.LIGHTGREEN_EX + "TABLE NAME: " + Fore.WHITE)
    d=""
    cls=[]
    try:
        d = Table(r, metadata, autoload=True, autoload_with=engine)
        cls=d.columns.keys()
        printf('|'.join(cls),Fore.GREEN)
    except:
        EDIT(1)
    col = input("what column you want to edit?: ")
    if col not in cls:EDIT(2)
    data = input("what is the new value of this column?: ").replace('"','\"')

    # [] TODO:  try to make the condition more efficent (beggeiners friendly)

    if guide_examples == True:
        printf("CONDITION:",Fore.CYAN) 
        printf("Example 1 : ID = 5",Fore.LIGHTMAGENTA_EX)
        printf("Example 2 : name='rami' OR name='john'",Fore.LIGHTMAGENTA_EX)
        printf("Example 3 : email='squar3@sqrt.dev' AND id=93",Fore.LIGHTMAGENTA_EX)

    cond = input("CONDITION: ")
    query = f'UPDATE {r} SET {col}="{data}" WHERE {cond}'

    try:
        rs = conn.execute(query)
        print(query)
        printf("DATA EDITED SUCCESSFULLY",Fore.GREEN)
    except:
        EDIT(3)

    input("PRESS ANY KEY TO GO BACK HOME!")
    Home()

def DELETE(inc=0):
    clear() 
    if(inc==1):printf("Incorrect table  name! ",Fore.RED)
    if(inc==2):printf("Incorrect condition! ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    printf("SELECT OPTION:",Fore.CYAN)
    r = input(Fore.LIGHTGREEN_EX + "TABLE NAME: " + Fore.WHITE)
    d=""
    cls=[]
    try:
        d = Table(r, metadata, autoload=True, autoload_with=engine)
        cls=d.columns.keys()
        printf('|'.join(cls),Fore.GREEN)
    except:
        DELETE(1)

    # [] TODO:  try to make the condition more efficent (beggeiners friendly)
    if guide_examples == True:
        printf("CONDITION:",Fore.CYAN) 
        printf("Example 1 : ID = 5",Fore.LIGHTMAGENTA_EX)
        printf("Example 2 : name='rami' OR name='john'",Fore.LIGHTMAGENTA_EX)
        printf("Example 3 : email='squar3@sqrt.dev' AND id=93",Fore.LIGHTMAGENTA_EX)

    cond = input("CONDITION: ")
    query = f'DELETE FROM {r} WHERE {cond}'
    try:
        rs = conn.execute(query)
        print(query)
        printf("DATA DELETED SUCCESSFULLY",Fore.GREEN)
    except:
       DELETE(2)

    input("PRESS ANY KEY TO GO BACK HOME!")
    Home()

def DESCRIBE():
    clear() 

    Home()

def BACKUP(inc=0):
    clear()
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    randomid=datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    path=config_path
    if path=='':
        path=os.getcwd()+'/'
    else:
        if path[-1]!='/':path+='/'
    os.system(f'mysqldump -u{username} -p{password} {database} > {path}backup-{randomid}.sql')

    printf(f"Backup created at {path}, You can change the path from the config.py file",Fore.GREEN)
    input("PRESS ANY KEY TO GO BACK HOME!")
    Home()

if __name__ == "__main__":
    Home()
