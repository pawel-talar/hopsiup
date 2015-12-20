drop table if exists users;
drop table if exists links;
drop table if exists comments;
drop table if exists tags;

create table users (
    id integer primary key autoincrement,
    login text not null unique,
    password text not null,
    info text not null,
    points interger not null
);

create table links (
    id integer primary key autoincrement,
    link text not null,
    title text not null,
    foreign key(user) references users(id)
);

create table comments (
    id integer primary key autoincrement,
    foreign key(link_id) references links(id),
    points integer not null
);

create table tags (
    id integer primary key autoincrement,
    name text not null
);
