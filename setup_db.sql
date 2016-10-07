\c postgres;
drop database if exists catalog_app;
create database catalog_app;
\c catalog_app;

create table users
  (id serial primary key,
    name varchar(255),
    social_id varchar(64),
    nickname varchar(64),
    email varchar(255),
    password varchar(255)
  );


create table catalogs
  (catalog_id serial primary key,
    catalog_name varchar(250),
    catalog_description varchar(1000),
    catalog_owner_id int references users (id)
  );

create table categories
  (category_id serial primary key,
    category_name varchar(100),
    category_description varchar(500),
    category_owner_id int references users (id)
  );

create table items
  (item_id serial primary key,
    item_name varchar(120),
    item_description varchar(1000),
    item_price float,
    item_owner_id int references users (id),
    item_category_id int references categories (category_id),
    item_catalog_id int references catalogs (catalog_id),
    item_photo_file_name varchar(512)
  );




-- Users
insert into users (name, email, social_id, password)
	values ('John', 'jdelaney01@gmail.com', '1', '12345');
insert into users (name, email, social_id, password)
	values ('Joe', 'jdelaney02@gmail.com', '2', '12345');
insert into users (name, email, social_id, password)
	values ('Julie', 'jdelaney03@gmail.com', '3', '12345');
insert into users (name, email, social_id, password)
	values ('Jane', 'jdelaney04@gmail.com', '4', '12345');
insert into users (name, email, social_id, password)
	values ('Jill', 'jdelaney05@gmail.com', '5', '12345');

-- Catalogs
insert into catalogs (catalog_name, catalog_owner_id) values('Winter 2016', 1);
insert into catalogs (catalog_name, catalog_owner_id) values('Spring 2016', 1);
insert into catalogs (catalog_name, catalog_owner_id) values('Summer 2016 - Outdoor', 1);
insert into catalogs (catalog_name, catalog_owner_id) values('Summer 2016 - Cooking', 1);
insert into catalogs (catalog_name, catalog_owner_id) values('Fall 2016 - Clothing', 1);


-- Categories
insert into categories (category_name, category_owner_id) values('Packs', 1);
insert into categories (category_name, category_owner_id) values('Tents', 1);
insert into categories (category_name, category_owner_id) values('Clothing', 1);
insert into categories (category_name, category_owner_id) values('Foot wear', 1);
insert into categories (category_name, category_owner_id) values('Appliances', 1);
insert into categories (category_name, category_owner_id) values('Main Course', 1);
insert into categories (category_name, category_owner_id) values('Appetizers', 1);
insert into categories (category_name, category_owner_id) values('Desert', 1);
insert into categories (category_name, category_owner_id) values('Beverages', 1);
insert into categories (category_name, category_owner_id) values('Beer & Wine', 1);


-- items
insert into items (item_name, item_price, item_owner_id, item_category_id, item_catalog_id)
	values ('Blue tent', 100.96, 1, 2, 3);
insert into items (item_name, item_price, item_owner_id, item_category_id, item_catalog_id)
	values ('Green pack', 125.65, 1, 1, 3);


select * from users;
select * from catalogs;
select * from categories;
select * from items;

