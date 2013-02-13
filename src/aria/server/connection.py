import sqlite3
import os

def connectDB(DBpath):
        if not(os.path.exists(os.path.dirname(DBpath))):
                os.makedirs(os.path.dirname(DBpath))
        if(os.path.exists(DBpath)):
                try:
                        conn=sqlite3.connect(DBpath)
                        return conn
                except sqlite3.OperationalError:
                        raise IOError('Unable to connect to database')
        else:
                try:
                        conn = sqlite3.connect(DBpath)
                except Exception, e:
                        print e
                        raise
                c = conn.cursor()
                print "Creating DB"
                c.executescript("""
                        create table clients(ClientID integer primary key,ClientName text,IP text not null);
                        create table users(userID integer primary key,userName text,IP text not null);
                        create table groups(GroupID integer primary key,GroupName text);
                        create table assoc(cID integer,gID integer,primary key(cID,gID));
                        create table clientconfig(password text);
                        create table auth (username string not null,password string not null);
                        """)
                c.execute("insert into clientconfig(password) values ('welcome')")
                conn.commit()
                return conn
