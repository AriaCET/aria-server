drop table if exists clients;
create table clients (
       id integer primary key autoincrement,
       num integer  not null,
       identifier string unique not null
);
