drop database if exists zoo;
create database zoo;
use zoo;

## Building ---------------------------------------------------------------------------------
drop table IF EXISTS zoo_user;
create table zoo_user (
 	email varchar(40) NOT NULL UNIQUE ,
	username varchar(40) NOT NULL UNIQUE,
	ppassword varchar(40) not null,
	usertype enum('admin', 'staff', 'visitor') default 'visitor' not null,

	primary key (email)
)ENGINE=INNODB;

drop table IF EXISTS admin;
create table admin (
	email varchar(40),
	username VARCHAR(40),
	PRIMARY KEY (email),
	foreign key (email) references zoo_user(email) ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=INNODB;

drop table IF EXISTS staff;
create table staff (
	email varchar(40),
	username VARCHAR(40),
	PRIMARY KEY (email),
	foreign key (email) references zoo_user(email) ON UPDATE CASCADE on DELETE CASCADE
)ENGINE=INNODB;

drop table IF EXISTS visitor;
create table visitor (
	email varchar(40),
	username VARCHAR(40),
	PRIMARY KEY (email),
	foreign key (email) references zoo_user(email) ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=INNODB;

drop table IF EXISTS exhibit;
create table exhibit (
	nname varchar(40), # not null unique
	waterfeature boolean not null,
	size int(11) not null,
    primary key (nname)
)ENGINE=INNODB;

drop table IF EXISTS animal;
create table animal (
	nname varchar(40) ,
	species varchar(40),
	animal_type ENUM('Amphibian', 'Bird', 'Fish', 'Invertebrate', 'Mammal', 'Reptile') not null,
	age int not null,
	animalexhibit varchar(40),
	primary key (nname, species),
	foreign key (animalexhibit) references exhibit(nname) on update cascade on delete restrict
)ENGINE=INNODB;

drop table IF EXISTS zoo_show;
create table zoo_show (
	nname varchar(40),
	dateandtime datetime,
	showexhibit varchar(40),
	showstaff varchar(40),
	showdate DATE,
	primary key (nname, dateandtime),
	foreign key (showexhibit) references exhibit(nname) on update cascade on delete RESTRICT,
	foreign key (showstaff) references staff(email)	on update cascade on delete cascade
)ENGINE=INNODB;

drop table IF EXISTS showvisits;
create table showvisits (
	email varchar (40),
	nname varchar(40),
	dateandtime datetime,
	primary key (email, nname, dateandtime),
	foreign key (email) references visitor(email)	on update cascade on delete cascade,
	foreign key (nname, dateandtime) references zoo_show(nname,dateandtime)	on update cascade on delete cascade
)ENGINE=INNODB;

drop table IF EXISTS exhibitvisits;
create table exhibitvisits (
	email varchar(40),
	nname varchar(40),
	dateandtime datetime,
	primary key (email, nname, dateandtime),
	foreign key (email) references visitor(email) on update cascade on delete cascade,
	foreign key (nname) references exhibit(nname) on update cascade on delete restrict
)ENGINE=INNODB;

drop table IF EXISTS note;
create table note (
	nname varchar(40),
	species varchar(40),
	email varchar (40),
	notetime datetime not null,
	notetext text,

	primary key (nname, species, email, notetime),
	foreign key (nname, species) references animal(nname, species) on update cascade on delete cascade,
	foreign key (email) references staff(email) on update cascade on delete cascade
)ENGINE=INNODB;
### ======================================================================================================

### functionality-----------------------------------------------------------------------------------------

## login and register=================================================================================
SELECT email, username FROM zoo_user where email = '' and username = '';
INSERT INTO zoo_user(email, username, ppassword, usertype) VALUES ('','','','','');
INSERT INTO admin(email, username) VALUES ('','');
INSERT INTO visitor(email, username) VALUES ('','');
INSERT INTO staff(email, username) VALUES ('','');
SELECT username, ppassword, usertype FROM zoo_user WHERE username='' AND ppassword=MD5('');

## sort===============================================================================================
# animal sort
SELECT nname, species, animalexhibit, age, animal_type from animal where nname = 'add any constraints here' ORDER BY nname ASC;
SELECT nname, species, animalexhibit, age, animal_type from animal where nname = 'add any constraints here' ORDER BY nname DESC;
# show sort
SELECT nname, showexhibit, dateandtime from zoo_show where nname = 'add any constraints here' ORDER BY nname ASC;
SELECT nname, showexhibit, dateandtime from zoo_show where nname = 'add any constraints here' ORDER BY nname DESC;
# exhibit
# SELECT AH, SIZE, NumAnimals, WF
# from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF
# 			from (select animalexhibit, size, waterfeature
# 						from (exhibit AS A JOIN animal B)
# 						where A.nname = B.animalexhibit)
# 				AS S
# 			GROUP BY animalexhibit)
# 	AS L where AH = 'and any constraints' ORDER BY AH ASC ;


# SELECT * from exhibit AS A  animal
SELECT L.A, L.B, L.C, L.D
FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D
			FROM exhibit
				LEFT JOIN animal
					ON exhibit.nname = animalexhibit
			GROUP BY exhibit.nname)
	AS L
WHERE L.A = '' and L.B = '' and L.C = '' and L.D = '';


SELECT A.nname, A.dateandtime, B.count
FROM exhibitvisits A
	INNER JOIN ((SELECT nname, count(*) as count
							 FROM exhibitvisits
							 GROUP BY nname)
		AS B)on A.nname = B.nname;



SELECT L.A, L.B, L.C
FROM (SELECT nname A, dateandtime B, count(nname) C
			from exhibitvisits
			WHERE email = ''
			GROUP BY (nname, dateandtime))
	AS L
WHERE exhibitvisits.nname = '';


SELECT A.nname, A.dateandtime, B.count FROM exhibitvisits A INNER JOIN ((SELECT nname, count(*) as count FROM exhibitvisits GROUP BY nname)AS B)on A.nname = B.nname WHERE email = 'visitor1@visitor';

## admin======================================================================================
#view visitor
SELECT username, email FROM visitor;
SELECT username, email from visitor ORDER BY email ASC;
DELETE FROM zoo_user where email = '';
#view staff
SELECT username, email FROM staff;
SELECT username, email from staff ORDER BY email ASC;
DELETE FROM zoo_user where email = '';
#view animal
SELECT nname, species, animalexhibit, age, animal_type from animal where nname = 'add any constraints';
DELETE from animal where nname = '' and species = '';
#view show
DELETE FROM zoo_show where nname = '' and dateandtime = '';
SELECT nname, showexhibit, dateandtime from zoo_show where nname = 'add any constraints';
#add show
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) values ('','','','','');
#add animal
INSERT into animal(nname, species, animal_type, age, animalexhibit) values('','','',0,'');

## visitor======================================================================================
#search exhibit
SELECT nname, species from animal where animalexhibit = '';
SELECT nname, species from animal where nname = '' ORDER BY nname ASC;
INSERT into exhibitvisits(email, nname, dateandtime) values ('','','');
SELECT AH, SIZE, NumAnimals, WF
from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF
			from (select animalexhibit, size, waterfeature
						from (exhibit AS A JOIN animal B)
						where A.nname = B.animalexhibit)
				AS S
			GROUP BY animalexhibit)
	AS L
where AH = '';
#search shows
SELECT nname, showexhibit, dateandtime from zoo_show where nname = '';
INSERT INTO showvisits(email, nname, dateandtime) values ('','','');
#search animals
SELECT nname, species, animalexhibit, age, animal_type from animal where nname = '';
#view exhibit history
SELECT L.A, L.B, L.C
FROM (SELECT nname A, dateandtime B, count(*) C
			from exhibitvisits
			GROUP BY nname, dateandtime)
	AS L
where L.A = '';
#show history
SELECT nname, showexhibit, dateandtime from zoo_show where nname = '';

## visitor======================================================================================
#search animal
SELECT email, notetext, notetime FROM note WHERE nname = '';
SELECT nname, species, animalexhibit, age, animal_type FROM animal where nname = '';
SELECT email, notetext, notetime FROM note where email = '' ORDER BY email ASC;
#view animal
SELECT nname, showexhibit, dateandtime FROM zoo_show where showstaff = '';

SELECT B.nname, A.dateandtime, B.nname
FROM (showvisits A JOIN zoo_show B)
WHERE A.nname = B.nname and A.email = '';

SELECT *
FROM exhibitvisits
WHERE email = '';

### populate=========================================
INSERT INTO zoo_user(email, username, ppassword, usertype) VALUES ('rqin37@gatech.edu', 'rqin37', MD5('12345678'),'admin');
INSERT INTO admin(email, username) VALUES ('rqin37@gatech.edu', 'rqin37');

INSERT INTO exhibit(nname, waterfeature, size) VALUES ('Pacific', TRUE , 850);
INSERT INTO exhibit(nname, waterfeature, size) VALUES ('Jungle', FALSE , 600);
INSERT INTO exhibit(nname, waterfeature, size) VALUES ('Sahara', FALSE , 1000);
INSERT INTO exhibit(nname, waterfeature, size) VALUES ('Mountainous', FALSE , 1200);
INSERT INTO exhibit(nname, waterfeature, size) VALUES ('Birds', TRUE , 1000);

INSERT INTO animal(nname, species, animal_type, age, animalexhibit) VALUES ('Goldy','Goldfish','Fish',1,'Pacific');
INSERT INTO animal(nname, species, animal_type, age, animalexhibit) VALUES ('Nemo','Clownfish','Fish',2,'Pacific');
INSERT INTO animal(nname, species, animal_type, age, animalexhibit) VALUES ('Pedro','Poison Dart frog','Amphibian',3,'Jungle');
INSERT INTO animal(nname, species, animal_type, age, animalexhibit) VALUES ('Lincon','Lion','Mammal',8,'Sahara');
INSERT INTO animal(nname, species, animal_type, age, animalexhibit) VALUES ('Greg','Goat','Mammal',6,'Mountainous');
INSERT INTO animal(nname, species, animal_type, age, animalexhibit) VALUES ('Brad','Bald Eagle','Bird',4,'Birds');

INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Jungle Cruise','18/10/06 9:00:00','Jungle','marthajohnson@hotmail.com','18/10/06');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Feed the Fish','18/10/08 12:00:00','Pacific','marthajohnson@hotmail.com','18/10/08');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Fun Facts','18/10/09 15:00:00','Sahara','marthajohnson@hotmail.com','18/10/09');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Jungle Cruise','18/10/12 14:00:00','Jungle','marthajohnson@hotmail.com','18/10/12');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Climbing','18/10/10 16:00:00','Mountainous','benjaminrao@gmail.com','18/10/10');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Flight of the Birds','18/10/11 15:00:00','Birds','ethanroswell@yahoo.com','18/10/11');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Feed the Fish','18/10/12 14:00:00','Pacific','ethanroswell@yahoo.com','18/10/12');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Fun Facts','18/10/13 13:00:00','Sahara','benjaminrao@gmail.com','18/10/13');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Climbing','18/10/13 17:00:00','Mountainous','benjaminrao@gmail.com','18/10/13');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Flight of the Birds','18/10/14 14:00:00','Birds','ethanroswell@yahoo.com','18/10/14');
INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) VALUES ('Bald Eagle Show','18/10/15 14:00:00','Birds','ethanroswell@yahoo.com','18/10/15');
