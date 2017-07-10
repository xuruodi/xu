
# Introduction to the data


```python
import sqlite3
conn = sqlite3.connect("nominations.db")
schema = conn.execute("pragma table_info(nominations);").fetchall()
first_ten = conn.execute("select * from nominations limit 10;").fetchall()

for r in schema:
    print(r)
    
for r in first_ten:
    print(r)
```

    (0, 'Year', 'INTEGER', 0, None, 0)
    (1, 'Category', 'TEXT', 0, None, 0)
    (2, 'Nominee', 'TEXT', 0, None, 0)
    (3, 'Won', 'INTEGER', 0, None, 0)
    (4, 'Movie', 'TEXT', 0, None, 0)
    (5, 'Character', 'TEXT', 0, None, 0)
    (2010, 'Actor -- Leading Role', 'Javier Bardem', 0, 'Biutiful', 'Uxbal')
    (2010, 'Actor -- Leading Role', 'Jeff Bridges', 0, 'True Grit', 'Rooster Cogburn')
    (2010, 'Actor -- Leading Role', 'Jesse Eisenberg', 0, 'The Social Network', 'Mark Zuckerberg')
    (2010, 'Actor -- Leading Role', 'Colin Firth', 1, "The King's Speech", 'King George VI')
    (2010, 'Actor -- Leading Role', 'James Franco', 0, '127 Hours', 'Aron Ralston')
    (2010, 'Actor -- Supporting Role', 'Christian Bale', 1, 'The Fighter', 'Dicky Eklund')
    (2010, 'Actor -- Supporting Role', 'John Hawkes', 0, "Winter's Bone", 'Teardrop')
    (2010, 'Actor -- Supporting Role', 'Jeremy Renner', 0, 'The Town', 'James Coughlin')
    (2010, 'Actor -- Supporting Role', 'Mark Ruffalo', 0, 'The Kids Are All Right', 'Paul')
    (2010, 'Actor -- Supporting Role', 'Geoffrey Rush', 0, "The King's Speech", 'Lionel Logue')
    

# Creating the ceremonies table


```python
years_hosts = [(2010, "Steve Martin"),
               (2009, "Hugh Jackman"),
               (2008, "Jon Stewart"),
               (2007, "Ellen DeGeneres"),
               (2006, "Jon Stewart"),
               (2005, "Chris Rock"),
               (2004, "Billy Crystal"),
               (2003, "Steve Martin"),
               (2002, "Whoopi Goldberg"),
               (2001, "Steve Martin"),
               (2000, "Billy Crystal"),
            ]
create_ceremonies = "create table ceremonies (id integer primary key, year integer, host text);"
conn.execute(create_ceremonies)
insert_query = "insert into ceremonies (Year, Host) values (?,?);"
conn.executemany(insert_query, years_hosts)

print(conn.execute("select * from ceremonies limit 10;").fetchall())
print(conn.execute("pragma table_info(ceremonies);").fetchall())
```

    [(1, 2010, 'Steve Martin'), (2, 2009, 'Hugh Jackman'), (3, 2008, 'Jon Stewart'), (4, 2007, 'Ellen DeGeneres'), (5, 2006, 'Jon Stewart'), (6, 2005, 'Chris Rock'), (7, 2004, 'Billy Crystal'), (8, 2003, 'Steve Martin'), (9, 2002, 'Whoopi Goldberg'), (10, 2001, 'Steve Martin')]
    [(0, 'id', 'integer', 0, None, 1), (1, 'year', 'integer', 0, None, 0), (2, 'host', 'text', 0, None, 0)]
    

# Foreign key constraints


```python
conn.execute("PRAGMA foreign_keys = ON;")
```




    <sqlite3.Cursor at 0x10675e3b0>



# Setting up one-to-many


```python
create_nominations_two = '''create table nominations_two 
(id integer primary key, 
category text, 
nominee text, 
movie text, 
character text, 
won text,
ceremony_id integer,
foreign key(ceremony_id) references ceremonies(id));
'''

nom_query = '''
select ceremonies.id as ceremony_id, nominations.category as category, 
nominations.nominee as nominee, nominations.movie as movie, 
nominations.character as character, nominations.won as won
from nominations
inner join ceremonies 
on nominations.year == ceremonies.year
;
'''
joined_nominations = conn.execute(nom_query).fetchall()

conn.execute(create_nominations_two)

insert_nominations_two = '''insert into nominations_two (ceremony_id, category, nominee, movie, character, won) 
values (?,?,?,?,?,?);
'''

conn.executemany(insert_nominations_two, joined_nominations)
print(conn.execute("select * from nominations_two limit 5;").fetchall())
```

    [(1, 'Actor -- Leading Role', 'Javier Bardem', 'Biutiful', 'Uxbal', '0', 1), (2, 'Actor -- Leading Role', 'Jeff Bridges', 'True Grit', 'Rooster Cogburn', '0', 1), (3, 'Actor -- Leading Role', 'Jesse Eisenberg', 'The Social Network', 'Mark Zuckerberg', '0', 1), (4, 'Actor -- Leading Role', 'Colin Firth', "The King's Speech", 'King George VI', '1', 1), (5, 'Actor -- Leading Role', 'James Franco', '127 Hours', 'Aron Ralston', '0', 1)]
    

# Deleting and renaming tables


```python
drop_nominations = "drop table nominations;"
conn.execute(drop_nominations)

rename_nominations_two = "alter table nominations_two rename to nominations;"
conn.execute(rename_nominations_two)
```




    <sqlite3.Cursor at 0x10675e6c0>



# Creating a join table


```python
create_movies = "create table movies (id integer primary key,movie text);"
create_actors = "create table actors (id integer primary key,actor text);"
create_movies_actors = '''create table movies_actors (id INTEGER PRIMARY KEY,
movie_id INTEGER references movies(id), actor_id INTEGER references actors(id));
'''
conn.execute(create_movies)
conn.execute(create_actors)
conn.execute(create_movies_actors)
```




    <sqlite3.Cursor at 0x10675e960>



# Populating the movies and actors tables


```python
insert_movies = "insert into movies (movie) select distinct movie from nominations;"
insert_actors = "insert into actors (actor) select distinct nominee from nominations;"
conn.execute(insert_movies)
conn.execute(insert_actors)

print(conn.execute("select * from movies limit 5;").fetchall())
print(conn.execute("select * from actors limit 5;").fetchall())
```

    [(1, 'Biutiful'), (2, 'True Grit'), (3, 'The Social Network'), (4, "The King's Speech"), (5, '127 Hours')]
    [(1, 'Javier Bardem'), (2, 'Jeff Bridges'), (3, 'Jesse Eisenberg'), (4, 'Colin Firth'), (5, 'James Franco')]
    

# Populating a join table


```python
pairs_query = "select movie,nominee from nominations;"
movie_actor_pairs = conn.execute(pairs_query).fetchall()

join_table_insert = "insert into movies_actors (movie_id, actor_id) values ((select id from movies where movie == ?),(select id from actors where actor == ?));"
conn.executemany(join_table_insert,movie_actor_pairs)

print(conn.execute("select * from movies_actors limit 5;").fetchall())
```

    [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4), (5, 5, 5)]
    


```python

```
