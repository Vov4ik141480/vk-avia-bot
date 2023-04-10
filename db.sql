create table user (
  id integer primary key,
  uid integer,
  first_name varchar(50),
  last_name varchar(50),
  bdate varchar(20),
  city varchar(50),
  contacts varchar(20),
  country varchar(20),
  domain varchar(50,
  sex varchar(20)
);

create table ticket (
  id integer primary key,
  departure_city varchar(20),
  destination_city varchar(20),
  depart_date varchar(20)
  user_id integer,
  foreign key (user_id) references user(id)
);