import sqlite3

conn = sqlite3.connect('gamestore.db')
cursor = conn.cursor()

cursor.executescript('''
    CREATE TABLE IF NOT EXISTS games (
        game_id      INTEGER PRIMARY KEY,
        title        TEXT    NOT NULL,
        genre        TEXT    NOT NULL,
        developer    TEXT    NOT NULL,
        release_year INTEGER,
        price        REAL    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name        TEXT    NOT NULL,
        country     TEXT    NOT NULL,
        age         INTEGER
    );

    CREATE TABLE IF NOT EXISTS purchases (
        purchase_id   INTEGER PRIMARY KEY,
        customer_id   INTEGER REFERENCES customers(customer_id),
        game_id       INTEGER REFERENCES games(game_id),
        purchase_date TEXT    NOT NULL,
        quantity      INTEGER DEFAULT 1
    );
''')

games = [
    (1,  'Elden Ring',            'RPG',        'FromSoftware',   2022, 59.99),
    (2,  'Cyberpunk 2077',        'RPG',        'CD Projekt Red', 2020, 49.99),
    (3,  'Hollow Knight',         'Indie',      'Team Cherry',    2017, 14.99),
    (4,  'Counter-Strike 2',      'Action',     'Valve',          2023,  0.00),
    (5,  'Stardew Valley',        'Simulation', 'ConcernedApe',   2016, 13.99),
    (6,  'Hades',                 'Indie',      'Supergiant',     2020, 24.99),
    (7,  'GTA V',                 'Action',     'Rockstar',       2013, 29.99),
    (8,  'The Witcher 3',         'RPG',        'CD Projekt Red', 2015, 39.99),
    (9,  'Terraria',              'Indie',      'Re-Logic',       2011,  9.99),
    (10, 'Red Dead Redemption 2', 'Action',     'Rockstar',       2019, 59.99),
    (11, 'Celeste',               'Indie',      'Maddy Thorson',  2018, 19.99),
    (12, 'FIFA 24',               'Sports',     'EA Sports',      2023, 59.99),
    (13, 'Minecraft',             'Simulation', 'Mojang',         2011, 26.99),
    (14, 'Dark Souls III',        'RPG',        'FromSoftware',   2016, 39.99),
    (15, 'Among Us',              'Indie',      'Innersloth',     2018,  4.99),
]

customers = [
    (1,  'Alex',   'Russia',  22),
    (2,  'Maria',  'Germany', 28),
    (3,  'John',   'USA',     35),
    (4,  'Yuki',   'Japan',   19),
    (5,  'Carlos', 'Brazil',  25),
    (6,  'Emma',   'UK',      31),
    (7,  'Pavel',  'Russia',  27),
    (8,  'Sophie', 'France',  23),
    (9,  'Ahmed',  'UAE',     29),
    (10, 'Mia',    'Canada',  21),
]

purchases = [
    (1,  1,  1,  '2024-01-15', 1),
    (2,  1,  3,  '2024-01-20', 1),
    (3,  2,  8,  '2024-01-22', 1),
    (4,  3,  7,  '2024-02-01', 1),
    (5,  4,  6,  '2024-02-03', 1),
    (6,  5,  2,  '2024-02-10', 1),
    (7,  6,  5,  '2024-02-14', 1),
    (8,  7,  1,  '2024-02-20', 1),
    (9,  8,  11, '2024-03-01', 1),
    (10, 9,  10, '2024-03-05', 1),
    (11, 10, 13, '2024-03-10', 1),
    (12, 1,  8,  '2024-03-15', 1),
    (13, 2,  6,  '2024-03-18', 1),
    (14, 3,  1,  '2024-03-22', 1),
    (15, 4,  9,  '2024-04-01', 1),
    (16, 5,  14, '2024-04-05', 1),
    (17, 6,  3,  '2024-04-10', 1),
    (18, 7,  5,  '2024-04-15', 1),
    (19, 8,  2,  '2024-04-20', 1),
    (20, 9,  12, '2024-04-25', 1),
    (21, 10, 7,  '2024-05-01', 1),
    (22, 1,  6,  '2024-05-05', 1),
    (23, 2,  1,  '2024-05-10', 1),
    (24, 3,  14, '2024-05-15', 1),
    (25, 4,  13, '2024-05-20', 1),
]

cursor.executemany('INSERT OR IGNORE INTO games     VALUES (?,?,?,?,?,?)', games)
cursor.executemany('INSERT OR IGNORE INTO customers VALUES (?,?,?,?)',     customers)
cursor.executemany('INSERT OR IGNORE INTO purchases VALUES (?,?,?,?,?)',   purchases)

conn.commit()
conn.close()

print('Database created.')
print(f'  {len(games)} games, {len(customers)} customers, {len(purchases)} purchases')
