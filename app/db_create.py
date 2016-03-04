import cx_Oracle
conn = cx_Oracle.connect('shreding/o@172.24.90.201:1521/orcl')
def getAllData():
    cur = conn.cursor()
    cur.execute('select * from XMLRelationalMapping')
    rows = cur.fetchall()
    return rows
def updateinConfig(t_name, c_name, d_type, uschecked, dbchecked):   
    sq="SELECT tablename,colname FROM XMLRELATIONALMAPPING where xpath=:xpath"
    cur1=conn.cursor()
    cur1.execute(sq,xpath=dbchecked)
    rows = cur1.fetchall()
    for row in rows:
        cur = conn.cursor()
        sql = "update XMLRelationalMapping set Xpath=:xpath where TableName=:tabname and ColName = :colname"
        cur.execute(sql, xpath = uschecked, tabname = row[0] , colname = row[1])
        conn.commit()
def updatedetailinConfig(t_name, ocname, c_name, d_type, xpath):    
    cur = conn.cursor()
    sql = "UPDATE XMLRelationalMapping SET ColName= :cname,DataType= :dtype where TableName=:tname and ColName=:ocname"
    cur.execute(sql, cname=c_name, dtype=d_type,tname=t_name,ocname=ocname)
    conn.commit()
def insertinConfig(t_name, c_name, d_type, xpath , onetoman ,splcol):  
    if(onetoman == ""):
        onetomany="N"
        rows = [ (t_name, c_name, d_type, xpath , 1 , onetomany , splcol )]
        cur1 = conn.cursor()
        cur1.executemany("insert into XMLRelationalMapping(TableName,ColName,DataType,Xpath,FILTER_IDENTIFIER,onetomany,SPL_COL) values (:1, :2, :3, :4, :5, :6, :7)", rows)
        conn.commit()
    else:
        onetomany="Y"
        rows = [ (t_name, c_name, d_type, xpath , 1 ,onetomany ,splcol)]
        cur1 = conn.cursor()
        cur1.executemany("insert into XMLRelationalMapping(TableName,ColName,DataType,Xpath,FILTER_IDENTIFIER,onetomany,SPL_COL) values (:1, :2, :3, :4, :5, :6, :7)", rows)
        conn.commit()   
def deleteinConfig(t_name, c_name, d_type, xpath):   
    sql = "delete from XMLRELATIONALMAPPING where TableName=:tname and ColName=:cname"
    cur = conn.cursor()
    cur.execute(sql, tname=t_name,cname=c_name)
    conn.commit()   
def getcnamefromconfig(dbchecked):
    sql="select ColName from XMLRelationalMapping where XPATH = :xpath";
    cur = conn.cursor()
    cur.execute(sql,xpath=dbchecked)   
    cname = cur.fetchall();
    return cname
def getTableName():   
    cur = conn.cursor()
    cur.execute("select Distinct TableName from XMLRelationalMapping")   
    rows = cur.fetchall();
    tables = rows
    return tables
def getAllXpaths():
    sql="select Xpath from XMLRelationalMapping";
    cur = conn.cursor()
    cur.execute(sql)  
    xpaths = cur.fetchall();
    return xpaths
def getSelectedTable(xpath):
    sxpath= "%" + xpath + "%"
    cur = conn.cursor()
    sql="select Distinct TableName from XMLRelationalMapping where XPATH LIKE :sxpath"
    cur.execute(sql,sxpath=sxpath)   
    table = cur.fetchall();
    return table
def getTargetTableDetails(t_name):
    tname=t_name.upper()
    cur = conn.cursor()
    cur.execute("select table_name from all_tables")   
    rows = cur.fetchall();
    for row in rows:
        if(row[0] == tname):
            sql="SELECT  column_name, data_type FROM all_TAB_COLUMNS WHERE table_name = :tname"
            cur1=conn.cursor()
            cur1.execute(sql,tname=row[0])
            tablecollist=cur1.fetchall()
            return tablecollist
def renameTargetTable(query):
    cur = conn.cursor()
    sql=query
    cur.execute(sql)
    conn.commit()
def addTargetTable(query):
    cur = conn.cursor()
    sql=query
    cur.execute(sql)
    conn.commit()
def updateTargetTable(query):
    cur = conn.cursor()
    sql=query
    cur.execute(sql)
    conn.commit()
def dropTargetTable(query):
    cur = conn.cursor()
    sql=query
    cur.execute(sql)
    conn.commit()
                
    
    
    
