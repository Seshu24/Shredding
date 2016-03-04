from flask import render_template, request, session, flash , jsonify
from app import app
import XpathCalc as xcalc
import db_create as db
from __builtin__ import str

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Sample Shredding')

@app.route('/xmlconfig', methods=['GET', 'POST'])
def xmlconfig():
    if request.method == 'GET':
        return render_template('index.html')
    xmlfile = request.form['xmlfile']
    session['xmlfile'] = xmlfile
    results = xcalc.xpathCalc(xmlfile)
    xpathlist = results.split(",")
    newxpathlist = []
    oxpath = []
    for xpath1 in xpathlist:
        newxpathlist.extend(xpath1.split())
    for x in newxpathlist:
        if "/" in x:
            oxpath.append(x)
    session['oxpath'] = oxpath
    noofxpath = len(oxpath)
    session['noofxpath'] = noofxpath
    rows = db.getAllData()
    noofrows = len(rows)
    tables = db.getTableName()
    return render_template('login.html',
                           title='XpathCalc', xmlfile=xmlfile, oxpath=oxpath, rows=rows, tables=tables, noofxpath=noofxpath, noofrows=noofrows)

@app.route('/update', methods=['GET', 'POST'])
def update():
    xmlfile = session.get('xmlfile')
    oxpath = session.get('oxpath')
    noofxpath = session.get('noofxpath')
    if request.method == 'GET':
        return render_template('index.html')
    t_name = request.form['tname']
    c_name = request.form['cname']
    d_type = request.form['dtype']
    uschecked = request.form['nxpath']
    dbchecked = request.form['oxpath']
    db.updateinConfig(t_name, c_name, d_type, uschecked, dbchecked)
    rows = db.getAllData()
    noofrows = len(rows)
    tables = db.getTableName()
    flash('Updated successfully')
    return render_template('login.html',
                           title='XpathCalc', xmlfile=xmlfile, oxpath=oxpath, rows=rows, tables=tables, noofxpath=noofxpath, noofrows=noofrows)
 
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    xmlfile = session.get('xmlfile')
    oxpath = session.get('oxpath')
    noofxpath = session.get('noofxpath')
    if request.method == 'GET':
        return render_template('index.html')
    t_name = request.form['tselect']
    c_name = request.form['colname']
    d_type = request.form['datatype']
    xpath = request.form['xpath']
    if('onetomany' in request.form):
        onetomany = request.form['onetomany']
    else:
        onetomany = ""
    if('splcol' in request.form):
        splcol=request.form['splcol']
        splcollist=splcol.split("/")
        if(len(splcollist)==7):
            if "@" in splcollist[6]:
                splcol = 7
            else:
                splcol = 6 
        elif(len(splcollist)==6):
            if "@" in splcollist[5]:
                splcol = 6
            else:
                splcol = 5 
        elif(len(splcollist)==5):
            if "@" in splcollist[4]:
                splcol = 5
            else:
                splcol = 4 
        elif(len(splcollist)==4):
            splcol = 4 
        elif(len(splcollist)==3):
            if "@" in splcollist[2]:
                splcol = 3
            else:
                splcol = 2       
    else:
        splcol = 1
    db.insertinConfig(t_name, c_name, d_type, xpath , onetomany ,splcol)
    script = "ALTER TABLE " + " " + t_name + " " + " ADD " + "  " + c_name + " " + d_type
    db.addTargetTable(script)
    rows = db.getAllData()
    noofrows = len(rows)
    tables = db.getTableName()
    flash('Inserted successfully')
    return render_template('login.html',
                           title='XpathCalc', xmlfile=xmlfile, oxpath=oxpath, rows=rows, tables=tables, noofxpath=noofxpath, noofrows=noofrows)
@app.route('/updatetable', methods=['GET', 'POST'])
def updatetable():
    xmlfile = session.get('xmlfile')
    oxpath = session.get('oxpath')
    noofxpath = session.get('noofxpath')
    if request.method == 'GET':
        return render_template('index.html')
    t_name = request.form['tname1']
    ocname = request.form['hiddenColumn']
    c_name = request.form['cname1']
    odtype = request.form['hiddentype']
    d_type = request.form['dtype1']
    xpath = request.form['sxpath']
    if(c_name != ocname):
        db.updatedetailinConfig(t_name, ocname , c_name, d_type, xpath)
        script = "ALTER TABLE" + " " + t_name + " " + "RENAME COLUMN " + "  " + ocname + " " + " TO " + " " + c_name;
        db.renameTargetTable(script)
        if(d_type != odtype):
            script1 = "ALTER TABLE " + " " + t_name + " " + "MODIFY " + " " + c_name + " " + d_type ;
            db.updateTargetTable(script1)
    else:
        db.updatedetailinConfig(t_name, ocname , c_name, d_type, xpath)
        if(d_type != odtype):
            script1 = "ALTER TABLE " + " " + t_name + " " + "MODIFY " + " " + c_name + " " + d_type ;
            db.updateTargetTable(script1)
    rows = db.getAllData()
    noofrows = len(rows)
    tables = db.getTableName()
    flash('Table Details updated Successfully')
    return render_template('login.html',
                           title='XpathCalc', xmlfile=xmlfile, oxpath=oxpath, rows=rows, tables=tables, noofxpath=noofxpath, noofrows=noofrows)
@app.route('/getSelectedTable')  
def getSelectedTable():
    a = request.args.get('a', "", type=str)
    b = a.split("/")
    c = b[1]
    d = b[2]
    xpath = "/" + c + "/" + d + "/"
    table = db.getSelectedTable(xpath)
    return jsonify(result=table)
@app.route('/deleterow', methods=['GET', 'POST'])
def deleterow():
    xmlfile = session.get('xmlfile')
    oxpath = session.get('oxpath')
    noofxpath = session.get('noofxpath')
    if request.method == 'GET':
        return render_template('index.html')
    t_name = request.form['tname2']
    c_name = request.form['cname2']
    d_type = request.form['dtype2']
    xpath = request.form['dxpath']
    db.deleteinConfig(t_name, c_name, d_type, xpath)
    script = "ALTER TABLE " + " " + t_name + " " + "DROP COLUMN " + " " + c_name
    db.dropTargetTable(script)
    rows = db.getAllData()
    noofrows = len(rows)
    tables = db.getTableName()
    flash('Deleted Successfully')
    return render_template('login.html',
                           title='XpathCalc', xmlfile=xmlfile, oxpath=oxpath, rows=rows, tables=tables, noofxpath=noofxpath, noofrows=noofrows)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
