class Dog:

    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
            """)

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute("DROP TABLE IF EXISTS dogs")

    def save(self):
        if self.id:
            CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))
        else:
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            self.id = CURSOR.lastrowid
        CONN.commit()
        return self

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        return Dog(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        return [cls.new_from_db(row) for row in CURSOR.fetchall()]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog:
            return dog
        else:
            return cls.create(name, breed)

    def update(self, name=None, breed=None):
        if name:
            self.name = name
        if breed:
            self.breed = breed
        self.save()

