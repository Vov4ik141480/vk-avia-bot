create table user (
  user_id integer primary key,
  first_name varchar(50),
  last_name varchar(50),
  mobile_phone varchar(20)
);

create table ticket (
  ticket_id integer primary key,
  departure_city varchar(20),
  destination_city varchar(20),
  depart_date varchar(20),
  search_date varchar(10),
  ticket_uid integer,
  foreign key(ticket_uid) references user(user_id)
);

create table iata_time_zone (
  iata_code varchar(5) primary key,
  time_zone varchar(50)
);