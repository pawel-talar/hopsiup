drop table if exists users;
drop table if exists links;
drop table if exists comments;
drop table if exists posts;
drop table if exists tags;
drop table if exists messages;

create table users (
    user_id integer primary key autoincrement,
    login text not null unique,
    password text not null,
    sex text not null default('-'),
    city text not null default('-'),
    age integer default(0),
    info text not null default(''),
    registered_on text not null default(date('now')),
    upoints integer not null default(0)
);

create table links (
    link_id integer primary key autoincrement,
    link text not null,
    title text not null,
    description text not null default 'brak opisu',
    user_id integer not null,
    lpoints integer not null default(0),
    added_on text not null default(date('now')),
    foreign key(user_id) references users(user_id)
);

create table comments (
    comment_id integer primary key autoincrement,
    link_id integer,
    cpoints integer not null default(0),
    added_on text not null default(date('now')),
    foreign key(link_id) references links(link_id)
);

create table posts (
    post_id integer primary key autoincrement,
    content text not null,
    ppoints integer not null default(0),
    user_id integer not null,
    added_on text not null default(date('now')),
    foreign key(user_id) references users(user_id)
);

create table tags (
    tag_id integer primary key autoincrement,
    name text not null,
    unumber integer not null default(0),
    pnumber integer not null default(0)
);

create table messages (
    mid integer primary key autoincrement,
    from_uid integer not null,
    to_uid integer not null,
    content text not null,
    sent_on text not null default(date('now')),
    foreign key(from_uid) references users(user_id),
    foreign key(to_uid) references users(user_id)
);
