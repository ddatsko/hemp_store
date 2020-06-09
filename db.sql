create table person(
    id serial primary key ,
    name varchar(100) not null ,
    surname varchar(100) not null ,
    phone varchar(20) not null ,
    bank_account varchar(50) not null ,
    mail varchar(50) not null,
    location varchar(100),
    password varchar(100)
);

create table agronom(
    id serial primary key ,
    debt int default 0,
    reputation int default 0,
    foreign key (id) references person (id)
);

create table buyer(
    id serial primary key,
    money int default 0,
    foreign key (id) references person (id)
);

create table packing_seller(
    id serial primary key,
    productivity_per_month int default 1000,
    foreign key (id) references person (id)
);

create table hemp(
    sort_id serial primary key ,
    sort_name varchar(100),
    days_growtime int,
    crop_capacity int,
    frost_resistance bool
);

create table packing(
    id serial primary key ,
    capacity_gr int,
    price int,
    manufacturer serial,
    foreign key (manufacturer) references packing_seller (id)
);

create table product(
    id serial primary key ,
    name varchar(100),
    price int,
    pack serial,
    min_age int default 18,
    foreign key (pack) references packing(id)
);

create table deals(
    id serial primary key ,
    seller serial,
    buyer serial,
    made date,
    successful bool,
    item serial,
    amount_of_product int,
    foreign key (seller) references agronom (id),
    foreign key (buyer) references buyer (id),
    foreign key (item) references product (id)
);

create table testing_table(
    id serial,
    seller serial,
    tester serial,
    made date,
    successful bool,
    product serial,
    amount int default 1,
    foreign key (seller) references agronom (id),
    foreign key (tester) references person (id),
    foreign key (product) references product (id)
);

create table feed_back(
    id serial,
    about serial not null ,
    author serial not null ,
    message varchar(200),
    about_order serial,
    made date,
    foreign key (about) references agronom (id),
    foreign key (author) references buyer (id),
    foreign key (about_order) references deals (id)
);

create table storage(
    id serial,
    owner serial,
    location varchar(100),
    name varchar(50) default null,
    capacity int default 0,
    foreign key (owner) references agronom (id)
);

create table field(
    id serial primary key ,
    owner serial,
    size int not null ,
    fertility_per_season int not null ,
    location varchar(50),
    current_sort serial,
    foreign key (current_sort) references hemp (sort_id),
    foreign key (owner) references agronom (id)
);

create table store_and_spend(
    owner serial,
    sort serial,
    amount int default 0,
    take bool default null,
    operation_day date default '01/01/2010',
    foreign key (owner) references agronom (id),
    foreign key (sort) references hemp (sort_id)
);

create table vacation(
    id serial primary key,
    destination serial,
    purpose varchar(100) default '-',
    departion date not null,
    arrival date not null,
    foreign key (destination) references field(id)
);

create table vacations(
    member serial,
    vacation serial,
    foreign key (member) references agronom(id),
    foreign key (vacation) references vacation(id)
);

create table ingredients(
    ingredient serial,
    product serial,
    amount_grams int,
    foreign key (ingredient) references hemp(sort_id),
    foreign key (product) references product(id)
);

create table admin(
    id serial,
    person_id serial,
    foreign key (person_id) references person(id)
);

insert into person (name, surname, phone, bank_account, mail, location, password)
 values
 ('Wendy', 'Terry', '+380*********', '439583989385938598', 'wterry@gmail.com', 'Rome, Italy', 'R`V=mT2C'),
 ('Neive', 'Hughes', '+8*********', '439583998457638598', 'nhughes@gmail.com', 'Baghdad, Iraq', '26}W}e_D'),
 ('Johnny', 'Mack', '+021*********', '349583998457638598', 'jmack@gmail.com', 'Cairo, Egypt', '4T})NzaZ'),
 ('Mira', 'Medrano', '+38*********', '934583998457638598', 'mmedrano@gmail.com', 'Cologne, Germany', '4]5Pr`E.'),
 ('Paris', 'Small', '+021*********', '934583998457638598', 'psmall@gmail.com', 'Kolkata, India', 'q]m}Z64c'),
 ('Nikita', 'Frame', '+042*********', '839984576385989345', 'nframe@gmail.com', 'Basra, Iraq', '3?7v&$JE'),
 ('Bevan', 'Gonzales', '+38*********', '859893458399845763', 'bgonzales@gmail.com', 'Curitiba, Brazil', '~e;-3Ez'),
 ('Pranav', 'Aguilar', '+7*********', '576385989345839984', 'paguilar@gmail.com', 'Shiraz, Iran', 'm)jXv3dH'),
 ('Enid', 'Douglas', '+088*********', '934583998457638599', 'edouglas@gmail.com', 'Fez, Morocco', '(B"!kQ3>'),
 ('Pascal', 'Rich', '+7*********', '763859934583998458', 'prich@gmail.com', 'Antalya, Turkey', 'GP9r%`/A'),
 ('Krzysztof', 'Freeman', '+38*********', '934586385983998457', 'kfreeman@gmail.com', 'Yokohama, Japan', '}c6^uM8u'),
 ('Kadeem', 'Potter', '+042*********', '399845763859893458', 'kpotter@gmail.com', 'Campinas, Brazil', 't54+7B#5'),
 ('Chelsy', 'Rivas', '+38*********', '934584576385983998', 'crivas@gmail.com', 'Bulawayo, Zimbabwe', 'Dg/](P4$'),
 ('Albi', 'Mcbride', '+600*********', '939984576385984583', 'amcbride@gmail.com', 'Zunyi, China', 'GMWz''9mJ'),
 ('Zahid', 'Murray', '+088*********', '938399845763859845', 'zmurray@gmail.com', 'Curitiba, Brazil', 'kz?8}&Qa'),
 ('Waqar', 'Horner', '+600*********', '934583993859884576', 'whorner@gmail.com', 'Dallas, USA', 'u)3z[RM#'),
 ('Emyr', 'Traynor', '+042*********', '934399845763859858', 'etraynor@gmail.com', 'Davao City, Philippines', 'a)d6LZ7y'),
 ('Emmeline', 'Thomson', '+38*********', '394583998457638598', 'ethomson@gmail.com', 'Brasília, Brazil', '}6zg;FE/'),
 ('Anayah', 'Mill', '+38*********', '934589398457638598', 'amill@gmail.com', 'Guadalajara, Mexico', '\FFaw8t5'),
 ('Harriet', 'Cochran', '+83*********', '934583995487638598', 'hcochran@gmail.com', 'Tianjin, China', '\FFaw8t4'),
 ('Jarred', 'Wharton', '+600*********', '936385458399845798', 'jwharton@gmail.com', 'Tijuana, Mexico', '\FFaw8t3'),
 ('Olly', 'Bell', '+38*********', '934545783998638598', 'obell@gmail.com', 'Wuhan, China', '\FFaw8t2'),
 ('Khia', 'Pate', '+38*********', '934583576385989984', 'kpate@gmail.com', 'Caracas, Venezuela', '\FFaw8t1'),
 ('Dakota', 'Edwards', '+600*********', '763859893458399845', 'dedwards@gmail.com', 'Dhaka, Bangladesh', '\FFaw8t0'),
 ('Darragh', 'Whitehouse', '+042*********', '934583598998457638', 'dwhitehouse@gmail.com', 'Omsk, Russia', '\FFaw8t-1'),
 ('Hashim', 'Barlett', '+088*********', '934583998457385986', 'hbarlett@gmail.com', 'Almaty, Kazakhstan', '\FFaw8t-2'),
 ('Aaisha', 'Strickland', '+38*********', '934583998457638589', 'astrickland@gmail.com', 'Peshawar, Pakistan', '\FFaw8t-3'),
 ('Hawwa', 'Carter', '+7*********', '934583998547638598', 'hcarter@gmail.com', 'Semarang, Indonesia', '\FFaw8t-4'),
 ('Ismaeel', 'Houston', '+38*********', '934853998457638598', 'ihouston@gmail.com', 'Jeddah, Saudi Arabia', '\FFaw8t-4'),
 ('Emmanuella', 'Serrano', '+7*********', '394583998457638598', 'eserrano@gmail.com', 'Astana, Kazakhstan', '\FFaw8t-5'),
 ('Ella', 'Busby', '+7*********', '934589398457638598', 'ebusby@gmail.com', 'Sofia, Bulgaria', '\FFaw8t-6');


insert into packing_seller (id, productivity_per_month)
    values
       (1, 20000),
       (2, 30000),
       (3, 22000),
       (4, 15000),
       (5, 44000),
       (6, 23000),
       (7, 11000),
       (8, 10000),
       (9, 7000),
       (10, 170000);

insert into agronom (id, debt, reputation)
    values
       (11, 0, 0),
       (12, 0, 0),
       (13, 0, 0),
       (14, 0, 0),
       (15, 0, 0),
       (16, 0, 0),
       (17, 0, 0),
       (18, 0, 0),
       (19, 0, 0),
       (20, 0, 0),
       (21, 0, 0);

insert into buyer (id, money)
    values
    (22, 40000),
    (23, 10000),
    (24, 25000),
    (25, 8000),
    (26, 12000),
    (27, 25000),
    (28, 30000),
    (29, 22000),
    (30, 15000),
    (31, 80000);

insert into packing(capacity_gr, price, manufacturer)
    values
    (10, 1, 1),
    (50, 5, 1),
    (25, 2, 2),
    (5, 1, 3),
    (30, 2, 4),
    (35, 4, 5),
    (110, 11, 6),
    (20, 2, 7),
    (30, 3, 8),
    (15, 1, 9),
    (20, 5, 9),
    (40, 4, 10),
    (60, 6, 10),
    (70, 7, 7),
    (95, 10, 8);

insert into product(name, price, pack, min_age)
    values
    ('hemb tea', 15, 1, 18),
    ('hemb seed', 2, 2, 21),
    ('hemb gum', 10, 4, 18),
    ('hemb flour', 40, 7, 14),
    ('hemb protein', 100, 15, 21),
    ('hemb balsam', 25, 13, 14),
    ('hemb shampoo', 5, 1, 18),
    ('hemb oil', 20, 10, 14),
    ('hemb bran', 18, 1, 18),
    ('hemb salt', 15, 7, 18);

insert into hemp (sort_name, days_growtime, crop_capacity, frost_resistance)
values
       ('West European Classic', 240, 50, false),
       ('East European Classic', 260, 35, true),
       ('North America Classic', 220, 75, true),
       ('South America Classic', 240, 70, false),
       ('Africa Classic', 230, 45, false),
       ('Asia Classic', 200, 35, true),
       ('White Dragon', 180, 55, true),
       ('Arab Miracle', 350, 95, false),
       ('Toronto Night', 200, 40, false),
       ('Tropic Pleasure', 120, 25, false);

insert into vacation (destination, departion, arrival)
    values
       ( 1, '04/18/2014', '04/28/2015'),
       ( 2, '01/24/2014', '05/05/2014'),
       ( 3, '04/15/2012', '04/29/2012'),
       ( 3, '11/13/2009', '11/25/2009'),
       ( 3, '07/03/2010', '07/23/2010'),
       ( 4, '08/25/2006', '01/05/2007'),
       ( 5, '05/17/2011', '05/27/2011'),
       ( 6, '01/10/2015', '01/12/2015'),
       ( 7, '04/11/2016', '05/11/2016'),
       ( 8, '02/20/2018', '02/28/2018'),
       ( 9, '02/20/2018', '02/28/2018'),
       ( 10, '02/20/2018', '02/28/2018'),
       ( 10, '02/20/2018', '02/28/2018'),
       ( 10, '02/20/2018', '02/28/2018');

insert into vacations (member, vacation)
values
       (11,15),
       (11,16),
       (12,17),
       (13,18),
       (11,19),
       (15,20),
       (16,21),
       (20,22),
       (21,23),
       (20,24),
       (14,25),
       (17,26),
       (12,27),
       (13,28);

insert into storage(owner, location, name, capacity)
values
       (11, 'Houston, USA', 'Spitzkop', 5000),
       (12, 'Hanoi, Vietnam', 'Water Edge', 7000),
       (13, 'Suwon, South Korea', 'Norwood Bottom', 10000),
       (14, 'Moscow, Russia', 'Allerton Oak', 20000),
       (15, 'Kobe, Japan', 'Cranleigh Drove', 25000),
       (16, 'Sapporo, Japan', 'Alpine Firs', 27000),
       (17, 'Karachi, Pakistan', 'Hopton Hall', 30000),
       (18, 'Hamburg, Germany', 'Sharesacre Street', 15000),
       (19, 'Lahore, Pakistan', 'Kay Estate', 13000),
       (20, 'Bucharest, Romania', 'Danescourt Road', 16000),
       (21, 'Chengdu, China', 'Cornwallis Circle', 18000),
       (21, 'Milan, Italy', 'Boroughdales', 15000);

insert into testing_table(seller, tester, made, successful, product, amount)
values
       (11, 22, '01/11/2011', true, 10, 2),
       (12, 23, '03/13/2013', true, 1, 3),
       (13, 23, '07/15/2014', true, 2, 4),
       (14, 24, '01/11/2015', true, 3, 5),
       (15, 25, '01/11/2016', true, 4, 6),
       (16, 26, '01/11/2017', true, 5, 7),
       (17, 27, '01/11/2018', true, 5, 8),
       (18, 28, '01/11/2019', true, 6, 9),
       (19, 31, '01/11/2020', true, 6, 8),
       (20, 30, '01/11/2020', true, 7, 7),
       (20, 30, '01/11/2020', true, 8, 6),
       (21, 31, '01/11/2020', true, 9, 5);

insert into field (owner, size, fertility_per_season, location, current_sort)
values
   (11, 50, 10, 'Houston, USA', 1),
   (12, 40, 12, 'Hanoi, Vietnam', 2),
   (13, 30, 13, 'Suwon, South Korea', 3),
   (14, 70, 20, 'Moscow, Russia', 4),
   (15, 50, 15, 'Kobe, Japan', 5),
   (16, 25, 13, 'Kobe, Japan', 6),
   (17, 30, 11, 'Karachi, Pakistan', 7),
   (18, 15, 11, 'Hamburg, Germany', 8),
   (19, 28, 18, 'Lahore, Pakistan', 9),
   (20, 80, 30, 'Bucharest, Romania', 1);

insert into ingredients(ingredient, product, amount_grams)
values
       (1, 1, 10),
       (1, 2, 40),
       (2, 1, 30),
       (2, 2, 40),
       (3, 3, 60),
       (4, 3, 15),
       (5, 3, 25),
       (6, 4, 40);

insert into store_and_spend(owner, sort, amount, operation_day, take)
values
       (11, 2, 100, '01/01/2014', false),
       (12, 2, 50, '01/01/2015', false),
       (13, 3, 200, '01/01/2016', false),
       (14, 4, 250, '01/01/2017', false),
       (15, 5, 125, '01/01/2017', false),
       (16, 6, 140, '01/01/2018', false),
       (17, 7, 190, '01/01/2019', false),
       (18, 8, 210, '01/01/2020', false),
       (19, 9, 200, '01/01/2018', false),
       (20, 2, 80, '01/01/2017', false),
       (21, 3, 90, '01/01/2016', false);

insert into deals (seller, buyer, made, successful, item, amount_of_product)
values
       (11, 22, '01/01/2019', false, 1, 3),
       (12, 23, '02/02/2019', false, 2, 2),
       (13, 24, '03/03/2019', false, 3, 1),
       (14, 25, '04/04/2019', true, 3, 4),
       (15, 26, '05/05/2019', true, 2, 5),
       (16, 27, '06/06/2019', true, 1, 6),
       (17, 28, '07/07/2019', true, 4, 1),
       (18, 29, '08/08/2019', true, 5, 2),
       (19, 30, '09/09/2019', true, 6, 3),
       (20, 31, '10/10/2019', true, 7, 7),
       (21, 30, '11/11/2019', true, 7, 4);

insert into feed_back (about, author, message, about_order, made)
values
       (12,22, 'Everything is good', 1, '01/01/2019'),
       (12,23, 'Everything is perfect', 2, '02/02/2019'),
       (13,24, 'Everything is magnificent', 3, '03/03/2019'),
       (14,25, 'Everything is ideal', 4, '04/04/2019'),
       (15,26, 'Everything is marvelous', 5, '05/05/2019'),
       (16,27, 'Everything is cool', 6, '06/06/2019'),
       (17,28, 'Everything is not good', 7, '07/07/2019'),
       (18,29, 'Everything is the best it could be', 8, '08/08/2019'),
       (19,30, 'Everything is ideal', 9, '09/09/2019'),
       (20,30, 'Everything is cool', 10, '09/09/2019'),
       (21,31, 'I liked everything', 11, '10/10/2019');

create INDEX person_index on person(id, name, surname, phone, bank_account, mail, location, password);

create INDEX buyer_index on buyer(id, money);

create INDEX seller_index on packing_seller(id, productivity_per_month);

create INDEX agronom_index on agronom(id, debt, reputation);

create INDEX deals_index on deals(id, seller, buyer, made, successful, item, amount_of_product);

create INDEX testing_index on testing_table(id, seller, tester, made, successful, product, amount);


-- delete from person;
-- delete from agronom;
-- delete from buyer;
-- delete from packing_seller;
-- delete from packing;
-- delete from hemp;
-- delete from product;
-- delete from deals;
-- delete from testing_table;
-- delete from feed_back;
-- delete from storage;
-- delete from field;
-- delete from store_and_spend;
-- delete from vacation;
-- delete from vacations;
-- delete from ingredients;
-- delete from admin;
--
--
-- drop table person cascade;
-- drop table agronom cascade;
-- drop table buyer cascade;
-- drop table packing_seller cascade;
-- drop table packing cascade;
-- drop table hemp cascade;
-- drop table product cascade;
-- drop table deals cascade;
-- drop table testing_table cascade;
-- drop table feed_back cascade;
-- drop table storage cascade;
-- drop table field cascade;
-- drop table store_and_spend cascade;
-- drop table vacation cascade;
-- drop table vacations cascade;
-- drop table ingredients cascade;
-- drop table admin cascade;

-- Query 1
-- Arguments: number 1 - N times that were sold; number 15 - particular agronom id we are interested in; dates - timeframes
select distinct buyer, b.name, b.surname from deals inner join agronom on deals.seller = agronom.id inner join person p on agronom.id = p.id inner join person b on deals.buyer = b.id
group by buyer, made, b.name, b.surname, seller HAVING count(buyer) >= 1 and seller = 20 and made > '01/01/2000' and made < '01/01/2020';

-- Query 2
-- Arguments: 31 - particular buyer id we are interested in; dates - timeframes
select distinct item, p.name from deals inner join buyer on deals.buyer = buyer.id inner join product p on deals.item = p.id where buyer.id = 31
                                                                    and made > '01/01/2000' and made < '01/01/2020';

-- Query 3
-- Arguments: 3 - N times product was tested, 23 particular consumer id;
select distinct agronom.id, p.name, p.surname from agronom inner join testing_table on agronom.id = testing_table.seller inner join person p on agronom.id = p.id
where  tester = 25 group by agronom.id, p.name, p.surname, made HAVING count(agronom.id) >= 1 and made > '01/01/2000' and made < '01/01/2020';

-- Query 4
-- Arguments:
select distinct vacations.member from
        vacations
    inner join
        (select distinct with_agronom.id as vacation from
            (select distinct vacation as id from vacations where member = 11)with_agronom
                inner join
            (select distinct id from vacation where (departion>'2010-01-01' and arrival<'2020-01-01'))within_date
            on with_agronom.id = within_date.id
        )chosen
    on vacations.vacation = chosen.vacation

-- Query 5
-- Arguments: 31 particular consumer id;
select distinct coalesce( deals.seller, tt.seller ) from deals inner join testing_table tt on deals.seller = tt.seller where deals.buyer = 31 or tt.tester = 31
and ( tt.made > '01/01/2000' or deals.made > '01/01/2000') and ( tt.made < '01/01/2022' or deals.made < '01/01/2022');

-- Query 6
-- Arguments: Number 2 - N items, we are interested in.
select buyer, p.name, p.surname from deals inner join person p on deals.buyer = p.id where made > '01/01/2000' and made < '01/01/2021' group by buyer, p.name, p.surname having count( distinct item ) >= 2;

-- Query 7
-- Arguments: 2 - N parameter in definition.
select owner, p.name, p.surname from store_and_spend inner join person p on p.id = owner where
take = false and operation_day > '01/01/2000' and operation_day < '01/01/2022'
group by owner, p.name, p.surname having count( distinct sort ) >= 2;

-- Query 8
-- Arguments: 25 - agronom id; 15 - buyer id.
select id from testing_table where tester = 25 and seller = 15 and made > '01/01/2000' and made < '01/01/2021';

-- Query 9 Not sure!
-- Arguments: 2 - N testers according to definition
select product, count( tester ) from testing_table where made > '01/01/2000' and made < '01/01/2021'
group by product having count( distinct tester ) > 2;

-- Query 10:
-- Arguments: 22 - id of the author we are interested in
select extract(month from made) as month, count(author) as feedbacks
from feed_back where author = 22 and made > '01/01/1999' and made < '01/01/2021' group by author, made;

-- Query 11:
-- Arguments: 2 - N parameter in definition
select current_sort, p.name, cast (a.harvest_taken as decimal) / count(current_sort) as harvest_per_vacations from vacation inner join vacations v on vacation.id = v.vacation inner join field f on vacation.destination = f.id inner join product p on p.id = current_sort
inner join (select sort, count(sort) as harvest_taken from store_and_spend group by sort) as a on current_sort = a.sort
where arrival > '01/01/2000' and arrival < '01/01/2025'
group by p.name, current_sort, a.harvest_taken  having count(current_sort) >= 2 order by harvest_per_vacations;

-- Query 12:
-- Arguments: 2 - M parameter in problem definition
select item, p.name from deals inner join product p on p.id = item where made > '01/01/2000' and made < '01/01/2021' group by p.name, deals.item having count( distinct buyer ) >= 2
order by cast( count(*) filter (where not successful) as decimal ) / count(*) desc ;