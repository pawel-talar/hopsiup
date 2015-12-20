drop table if exists users;
drop table if exists links;
drop table if exists comments;
drop table if exists tags;

create table users (
    id integer primary key autoincrement,
    login text not null unique,
    password text not null,
    info text not null,
    points integer not null
);

create table links (
    id integer primary key autoincrement,
    link text not null,
    title text not null,
    user_id integer,
    foreign key(user_id) references users(id)
);

create table comments (
    id integer primary key autoincrement,
    link_id integer,
    points integer not null,
    foreign key(link_id) references links(id)
);

create table tags (
    id integer primary key autoincrement,
    name text not null
);
