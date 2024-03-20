create table Users (
 id integer primary key,
 name varchar(100),
 username varchar(50) unique
);

create table Tasks (
 id uuid default gen_random_uuid() primary key,
 user_id integer references Users on delete cascade,
 name varchar(100) not null,
 description text,
 is_done boolean not null,
 created_at timestamp not null
);

create table UsersStates (
 user_id integer primary key,
 state varchar (50) not null
);
