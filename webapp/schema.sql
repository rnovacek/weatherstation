drop table if exists record;
create table record (
    id integer primary key autoincrement,
    'datetime' datetime not null,
    battery real,
    sequence integer,
    node integer
);

drop table if exists measurement;
create table measurement (
    id integer primary key autoincrement,
    record int,
    sensor varchar(32),
    temperature real,
    humidity real
);
