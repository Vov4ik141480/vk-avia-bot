create table user (
  id integer primary key,
  uid integer,
  first_name varchar(50),
  last_name varchar(50),
  mobile_phone varchar(20),
);

create table ticket (
  id integer primary key,
  departure_city varchar(20),
  destination_city varchar(20),
  depart_date varchar(20)
  user_id integer,
  foreign key (user_id) references user(id)
);