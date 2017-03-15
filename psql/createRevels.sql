-- postgresql (9.6) psql file for creation of revels dataset.

create schema revels;
set search_path to revels;

-- Record origin of bags
create table shops (
  id          serial primary key,
  shop_name   text not null,
  address_1   text,
  address_2   text,
  address_3   text,
  postcode    text not null
);

-- Insert the shops already known into the table.
insert into shops (shop_name, address_1, address_2, address_3, postcode)
  values ('Tesco Express','Saffron Square','Wellsley Road','Croydon','CR9 2BY');
insert into shops (shop_name, address_1, address_2, address_3, postcode)
  values ('Spar','93 - 95 High Street','Porthmadog','Wales','LL49 9EU');
insert into shops (shop_name, address_1, address_2, address_3, postcode)
  values ('Riverside Shopping Centre', 'Pride Hill Centre',
          'Shrewsbury', 'Shropshire', 'SY1 1BU')
-- insert into shops (shop_name, address_1, address_2, address_3, postcode)
  -- values ('The cooperative','','','Wem','SY4 5XX');


-- Record bag data
create table bags (
  id          serial primary key,
  shop_bought integer not null references shops(id),
  total_mass  real not null,
  price       real not null
);


insert into bags (shop_bought, total_mass, price)
  values (1,112,1);
insert into bags (shop_bought, total_mass, price)
  values (2,112,1);
insert into bags (shop_bought, total_mass, price)
  values (2,112,1);
insert into bags (shop_bought, total_mass, price)
  values (3,112,1);



-- Types table
create table types (
  id          serial primary key,
  type_name   text not null
);

-- Populate the types table, as all values are already known.
insert into types (type_name) values ('Raisin');
insert into types (type_name) values ('Toffee');
insert into types (type_name) values ('Orange');
insert into types (type_name) values ('Coffee');
insert into types (type_name) values ('Malteser');
insert into types (type_name) values ('Galaxy Counter');

-- Main revels data table
create table data (
  id          serial primary key,
  bag_id      integer not null references bags(id),
  type_id     integer not null references types(id),
  mass        real not null,  -- Expressed in grams.
  density     real not null,  -- Expressed in g/cm3.
  height      real not null,  -- in millimeters.
  width       real not null,  -- in millimeters.
  depth       real not null  -- in millimeters.
);

-- create a bags view with the shop it was bought at as well.
create view bags_detail as
select bags.id, total_mass, price, shop_name, address_1, address_2, address_3,
postcode from bags join shops on bags.shop_bought=shops.id;

-- create a revels view
create view revels_detail as
select data.id as data_id, bags.id as bag_id, shops.id as shop_id,
types.type_name, data.mass, data.density, data.height, data.width, data.depth
from data join bags on data.bag_id=bags.id 
join shops on shops.id=bags.id 
join types on types.id=data.type_id;

