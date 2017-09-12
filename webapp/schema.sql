drop table if exists temperature;
create table temperature (
    id integer primary key autoincrement,
    'datetime' datetime not null,
    temperature real,
    humidity real,
    battery real,
    sequence integer,
    node integer
);
