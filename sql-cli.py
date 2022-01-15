#! /usr/bin/python
try:
    from prettytable import PrettyTable 
    import inquirer
    from inquirer.themes import GreenPassion
    from sqlalchemy import*
    from sqlalchemy.sql import text
    from config import*
    from colorama import Fore
    import time,os,inspect
    from datetime import datetime 
    from simple_term_menu import TerminalMenu as TM
    from sys import argv
    import sys
except:
    print("Error importing modules.\nTrying to install the required modules...\n") 
    path='./'
    if str(__file__).count('/') != 0:
        path=__file__[0:__file__.rfind('/')]+'/'
    __import__("os").system("python3 -m pip install -r requirements.txt")
    print("\nPlease restart the script or try installing the modules manually!")
    exit()

def printf(msg,color=Fore.WHITE):
    print(color + msg + Fore.WHITE)

def Help():
    print("""sql-cli help menu
    -h | --help             Show this message
    -p | --password         Enter the sql password instead of saving it!
    """)             
    exit()

if len(argv) > 1:
    if argv[1] in ("-h","--help"):
        Help()
    elif argv[1] in ("-p","--password"):
        password = input("Enter sql password: ")
    else:
        printf(f"Argument not expected: {argv[1]}",Fore.RED)
        Help()


def clear(force=False):
    if allow_clear_console==True or force==True:
        if os.name == 'nt':os.system('cls')
        else: os.system('clear') 
clear(True)

#Sql injection warning
if sqli_warning==True: 
    printf("THIS PRODUCT SHOULD BE AVALIABLE ONLY FOR ADMINSTARTORS, IT IS NOT PROTECTED AGAINST SELF-SQL INJECTIONS!",Fore.RED)
    printf(f"if you want to hide this message. please set sqli_warning to {Fore.GREEN}False{Fore.YELLOW} in {Fore.GREEN}config.py{Fore.YELLOW}\n",Fore.YELLOW)
    time.sleep(1)
    printf("Trying to connect to database using config.py",Fore.YELLOW)


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


#Setup
conn = False
metadata = 0
engine = create_engine('mysql+pymysql://'+username+':'+password+'@'+host+'/'+database)

def Refresh():
    try:
        conn = False
        metadata = 0
        engine = create_engine('mysql+pymysql://'+username+':'+password+'@'+host+'/'+database)
        conn = engine.connect()
        metadata = MetaData()
    except:
        pass

#Database connection
printf("Connecting to database",Fore.YELLOW)
try:
    conn = engine.connect()
    metadata = MetaData()
    printf("Connected successfully!",Fore.GREEN)
except:
    printf("Error while conncting to database..",Fore.RED)
    yn = input(f"{Fore.WHITE}Do you want to setup your database? [{Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}]: ")
    if yn == '' or yn.upper() == 'Y':
        path='./'
        if str(__file__).count('/') != 0:
            path=__file__[0:__file__.rfind('/')]+'/'
        os.system('${VISUAL-${EDITOR-nano}} '+path+'config.py')
        exit(1)
    else:exit(1)


#Functions
def debug(msg,errorLevel=0):
    if debugLog == True:
        if errorLevel == 0:
            printf(msg,Fore.GREEN)

def StringTuple(tp):
    b=()
    for i in tp:
        b = b + (str(i),)
    return b


#Program
def Home(inc=0):
    Refresh()
    clear()
    if(inc==1):printf("Incorrect option: ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    options = ["[1] VIEW","[2] INSERT","[3] EDIT","[4] DELETE","[5] ALTER","[6] DESCRIBE","[7] BACKUP","[8] Configure","[9] EXIT"]
    mainMenu = TM(options,title="Home")
    r = str(mainMenu.show() + 1)
    if   r=='1':VIEW()
    elif r=='2':INSERT()
    elif r=='3':EDIT()
    elif r=='4':DELETE()
    elif r=='5':ALTER()
    elif r=='6':DESCRIBE()
    elif r=='7':BACKUP()
    elif r=='8':Configure()
    elif r=='9':exit()
    else:Home(1)

def VIEW(inc=0):
    clear()
    Refresh()
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
    except:
        VIEW(1)
    
    #print(Fore.LIGHTGREEN_EX+"Columns -> "+Fore.YELLOW +"DEFAULT("+",".join(cls)+")"+Fore.WHITE)
    #b = input(Fore.LIGHTGREEN_EX+"Columns: "+Fore.WHITE)

    #checkbox
    debug('<Space> to select\n<Enter> to submit')
    questions = [
    inquirer.Checkbox('rows',
                    message="What features do you want in your column?",
                    choices=cls,
                ),
    ]
    bb = inquirer.prompt(questions,theme=GreenPassion())
    b = ",".join(bb['rows'])

    if b=="":b=",".join(cls) # ALL COLUMNS
    query = text(f"SELECT {b} FROM {r};")
    
    try:
        rs = conn.execute(query)
    except:
    
        VIEW(2)

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
    if debugLog == True:
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

def DESCRIBE(inc=0):
    clear() 
    
    #Select table section
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables =[] #tables
    for i in conn.execute(query):tables.append(str(i)[2:-3])
    menu = TM(tables,title="SELECT TABLE")
    r = tables[menu.show()]
   
    #GET COLUMNS DETAILS
    rows = 'COLUMN_NAME,COLUMN_DEFAULT,IS_NULLABLE,COLUMN_TYPE,COLUMN_KEY,EXTRA'
    query   = f"SELECT {rows} FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = '{r}' "
    
    columns = []
    rows = 'NAME,DEFAULT,IS_NULL,TYPE,KEY,EXTRA'
    myTable = PrettyTable(rows.split(','))
    for i in conn.execute(query):
        myTable.add_row(list(i))

    print(myTable)
    
    #Basicly mix CHARACTER_MAXIMUM_LENGTH and NUMERIC_PRECISION because they cannot be set at the same time (BUT WE ARE NOT SHOWING LENGTH ANYMORE)
    #fixed_columns = [] 
    #for i in range(len(columns)): 
    #    if str(columns[i][4]) == "None":
    #        fixed_columns.append(columns[i][0:4] + columns[i][5:])
    #    else:
    #        fixed_columns.append(columns[i][0:5] + columns[i][6:])



    Home()

def ALTER(inc=0,err=""):
    clear()
    if(inc==1):printf("Incorrect table  name! ",Fore.RED)
    if(inc==2):printf("Incorrect condition! ",Fore.RED)
    if(inc==3):printf(f"Error in DATATYPE paramater '{err}' ! ",Fore.RED)
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    printf("SELECT OPTION:",Fore.CYAN)

    #Select table section
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables =[] #tables
    for i in conn.execute(query):tables.append(str(i)[2:-3])
    menu = TM(tables,title="SELECT TABLE")
    r = tables[menu.show()]
    
    #Select alter options
    options =["Add column","Delete column"]
    menu = TM(options,title="SELECT AN OPTION")
    o = menu.show()
    
    if o == 0:#add_column
        column_name = ""
        while column_name == "": column_name = input("Please enter the name of the column you want to add: ") #COLUMN_NAME

        options =["INT(~)","VARCHAR(~)","TEXT","DATE","FLOAT(~,~)","TINY_INT","OTHER"] #COLUMN_TYPE
        menu = TM(options,title="SELECT AN OPTION")
        dt = options[menu.show()]
        
        # Settings default values
        default = ""
        if "INT(~)" == dt:          default = "10"
        elif "FLOAT(~,~)" == dt:    default = "n,x"
        elif "VARCHAR(~)" == dt:    default = "255"

        if default != "": #If the type takes some arguments I won't leave it empty 
            df = input(f"Enter arguments for {dt} or leave it empty for default ({default}): ") # Taking new default value 
            if df != "":    default = df # Changing the default value if the input isn't empty 
            for x in df:
                if x not in "1234567890,.":ALTER(inc=3, err=df)
        
        column_type = dt[:dt.find("(")] + f"({default})"

        #checkbox
        debug('<Space> to select\n<Enter> to submit')
        questions = [
          inquirer.Checkbox('features',
                            message="What features do you want in your column?",
                            choices=['NOT NULL','PRIMARY KEY','AUTO_INCREMENT'],
                            ),
        ]
        states = inquirer.prompt(questions,theme=GreenPassion())

        printf("Please enter a default value! (PRESS ENTER FOR NULL)",Fore.YELLOW)
         
        default_value = input("Default value: ")
        if default_value == "":
            query = f"ALTER TABLE {r} ADD {column_name} {column_type} "
            for st in states['features']:query+=f"{st} "  #adding states to the query
            conn.execute(query)
        else:
            query = f"ALTER TABLE {r} ADD {column_name} {column_type} DEFAULT %s "
            for st in states['features']:query+=f"{st} "  #adding states to the query
            conn.execute(query,(default_value))

    elif o == 1:#delete_column
        cls=[]
        d = Table(r, metadata, autoload=True, autoload_with=engine)
        cls=d.columns.keys()

        debug('<Space> to select\n<Enter> to submit')
        questions = [
        inquirer.List('rows',
                        message="Which column you want to delete??",
                        choices=cls,
                    ),
        ]
        column = inquirer.prompt(questions,theme=GreenPassion())['rows']


        yn = input(f"{Fore.WHITE}Are you sure you want to delete the column '{column}'? [{Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}]: ")
        if yn == "Y" or yn =="":
            query = f"ALTER TABLE {r} DROP COLUMN {column}"
            conn.execute(query)

    Home()

def BACKUP(inc=0):
    clear()
    printf("MODE: " + inspect.getframeinfo(inspect.currentframe()).function ,Fore.YELLOW)
    randomid=datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    path=config_path
    if path=='':
        if str(__file__).count('/') != 0:
            path=__file__[0:__file__.rfind('/')]+'/'
    else:
        if path[-1]!='/':path+='/'
    os.system(f'mysqldump -u{username} -p{password} {database} > {path}backup-{randomid}.sql')

    printf(f"Backup created at {path}, You can change the path from the config.py file",Fore.GREEN)
    input("PRESS ANY KEY TO GO BACK HOME!")
    Home()

def Configure(inc=0):
    clear()
    path='./'
    if str(__file__).count('/') != 0:
        path=__file__[0:__file__.rfind('/')]+'/'
    os.system('${VISUAL-${EDITOR-nano}} '+path+'config.py')
    Home()


if __name__ == "__main__":
    Home()
