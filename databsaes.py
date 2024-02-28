import sqlite3

conncet = sqlite3.connect('tracker.db')
c = conncet.cursor()
c.execute("""CREATE TABLE exercises (
        id integer primary key,
        exercise text not null
    )""")

c.execute("""CREATE TABLE data (
          id integer primary key,
          weight integer not null,
          exercise_id integer not null,
          foreign key (exercise_id) references exercises(id)
)""")