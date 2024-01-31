import sqlite3

CONN = sqlite3.connect(':memory:')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS dogs
            (id INTEGER PRIMARY KEY, name TEXT, breed TEXT)
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
        self.id = CURSOR.lastrowid  # Assign the generated id to the instance
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        # Ensure correct order of attributes in the tuple (id, name, breed)
        return cls(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        return [cls(*row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ? LIMIT 1", (name,))
        row = CURSOR.fetchone()
        return cls(*row) if row else None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id = ? LIMIT 1", (id,))
        row = CURSOR.fetchone()
        return cls(*row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name_and_breed(name, breed)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    @classmethod
    def find_by_name_and_breed(cls, name, breed):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1", (name, breed))
        row = CURSOR.fetchone()
        return cls(*row) if row else None

    def update(self):
        if self.id:
            CURSOR.execute("UPDATE dogs SET name=?, breed=? WHERE id=?", (self.name, self.breed, self.id))
            CONN.commit()
        else:
            raise ValueError("Cannot update record without id")
