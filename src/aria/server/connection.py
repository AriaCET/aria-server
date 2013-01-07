import sqlite3
import os

def connectDB(DBpath):
        if not(os.path.exists(os.path.dirname(DBpath))):
                raise IOError('Invalid database path_1')

        if(os.path.exists(DBpath)):
                try:
                        conn=sqlite3.connect(DBpath)
                        return conn
                except sqlite3.OperationalError:
                        raise IOError('Unable to connect to database')
        else:
                conn = sqlite3.connect(DBpath)
                c = conn.cursor()
                print "Creating DB"
                c.executescript("""
                        create table clients(ClientID integer primary key,ClientName text,IP text not null);
                        create table groups(GroupID integer primary key,GroupName text);
                        create table assoc(cID integer,gID integer,primary key(cID,gID));
                        create table clientconfig(password text);
                        create table auth (username string not null,password string not null);
                        """)
                c.execute("insert into clientconfig(password) values ('welcome')")
                conn.commit()
                return conn
