create table user (
  id integer primary key,
  uid integer NOT NULL UNIQUE,
  first_name varchar(255),
  last_name varchar(255),
  mobile_phone varchar(255)
);

create table ticket (
  id integer primary key,
  departure_city varchar(255),
  destination_city varchar(255),
  depart_date varchar(255),
  user_id integer,
  foreign key (user_id) references user(id)
);