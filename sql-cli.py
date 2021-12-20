#! /usr/bin/env python
from prettytable import PrettyTable 
from sqlalchemy import*
from sqlalchemy.sql import text
from config import*
from colorama import Fore
import time,os,inspect
from datetime import datetime 
from simple_term_menu import TerminalMenu as TM

def printf(msg,color=Fore.WHITE):
    print(color + msg + Fore.WHITE)

def clear(force=False):
    if allow_clear_console==True or force==True:
        if os.name == 'nt':os.system('cls')
        else: os.system('clear') 
clear(True)

#Sql injection warning
if sqli_warning==True: 
    printf("THIS PRODUCT SHOULD BE AVALIABLE ONLY FOR ADMINSTARTORS, IT IS NOT PROTECTED AGAINST SELF-SQL INJECTIONS!",Fore.RED)
    printf("Sql-cli will start in 3 seconds..",Fore.YELLOW)
    printf("if you want to hide this message. please set sqli_warning to False in config.py",Fore.YELLOW)
    time.sleep(3)
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

def StringTuple(tp):
    b=()
    for i in tp:
        b = b + (str(i),)
    return b

#Program
def Home(inc=0):
    clear()
    if(inc==1):printf("Incorrect option: ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    options = ["[1] VIEW","[2] INSERT","[3] EDIT","[4] DELETE","[X] DESCRIBE","[6] BACKUP","[7] EXIT"]
    mainMenu = TM(options,title="Home")
    r = str(mainMenu.show() + 1)
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
    #list all tables
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables =[]
    for i in conn.execute(query):tables.append(str(i)[2:-3])
    menu = TM(tables,title="SELECT TABLE")
    r = tables[menu.show()]
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
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables =[]
    for i in conn.execute(query):tables.append(str(i)[2:-3])
    menu = TM(tables,title="SELECT TABLE")
    r = tables[menu.show()]
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

    insertedData = []
    for cl in cls:
        CL = input(cl+": ")
        if CL != "":
            data += ' %s ' + ',' #Common self-defense sqli (NOT SECURE AT ALL)
            cols += cl + ',' 
            insertedData.append(CL)
            print(insertedData)

    data=data[:-1];cols=cols[:-1]
    newData = tuple(insertedData)
    query = f'INSERT INTO {r}({cols}) VALUES({data})'

    try:
        rs = conn.execute(query,newData)
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

    #Select table section
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables =[] #tables
    for i in conn.execute(query):tables.append(str(i)[2:-3])
    menu = TM(tables,title="SELECT TABLE")
    r = tables[menu.show()]
    
    d = Table(r, metadata, autoload=True, autoload_with=engine)
    cls=d.columns.keys() #columns

    query = text(f"SELECT * FROM {r} ORDER BY {str(cls[0])}")
    members=[]
    conds=[]
    ix=0
    for i in conn.execute(query):
        members.append(','.join(StringTuple(i)))
        conds.append([])
        for rw in i:
            conds[ix].append(rw)
        ix+=1
        
        
    menu = TM(members,title="SELECT THE ROW: ") 
    condi = menu.show()
    time.sleep(0.5)
    
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    menu = TM(cls,title="SELECT COLUMN")
    col = cls[menu.show()]

    inf=[]
    for i in range(len(cls)):inf.append(str(conds[condi][i])) #Filling the data into the array
    inf = tuple(inf) #Converting the array to tuple
    #cls,#inf

    #Generate the condition
    whereCond = "WHERE "
    for cl in cls:
        whereCond += f" {cl} = %s AND"
    whereCond = whereCond[:-3]
    print(inf)

    data = input("what is the new value of this column?: ")
    # [] TODO:  try to make the condition more efficent (beggeiners friendly)

    #data,inf
    finalInf = (data,) + inf 
    #Final query
    query = f'UPDATE {r} SET {col}=%s {whereCond}'

    try:
        rs = conn.execute(query,finalInf)
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

    #Select table section
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables =[] #tables
    for i in conn.execute(query):tables.append(str(i)[2:-3])
    menu = TM(tables,title="SELECT TABLE")
    r = tables[menu.show()]
    
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
