import cx_Oracle

conn = cx_Oracle.connect('shreding/o@172.24.90.201:1521/orcl')

    
rows = [ ('book_master', 'book_id', 'Varchar(10)', '/bookstore/book/bookid'),
         ('book_master', 'book_name', 'Varchar(20)', '/bookstore/book/bookname'),
         ('book_master', 'book_author', 'Varchar(20)', '/bookstore/book/bookauthor'),
         ('book_master', 'book_price', 'Number(8)', '/bookstore/book/bookprice'),
         ('book_master', 'published_Year', 'Number(4)', '/bookstore/book/year'),
         ('book_dealer', 'dealer_id', 'Varchar(10)', '/bookstore/dealer/id'),
         ('book_dealer', 'dealer_name', 'Varchar(15)', '/bookstore/dealer/name'),
         ('book_dealer', 'published_book', 'Varchar(15)', '/bookstore/dealer/bookpublished')]

cur = conn.cursor()
cur.executemany("insert into XMLRelationalMapping(TableName,ColName,DataType,Xpath) values (:1, :2, :3, :4)", rows)
conn.commit()
print "Records created successfully"
cur2 = conn.cursor()
cur2.execute('select * from XMLRelationalMapping')
rows = cur2.fetchall()
print rows
cur.close()
conn.close()
