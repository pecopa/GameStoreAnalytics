import sqlite3

conn = sqlite3.connect('gamestore.db')
cursor = conn.cursor()


def show(title, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description]

    print(f'\n--- {title} ---')
    print('  '.join(f'{c:<22}' for c in cols))
    print('-' * 60)
    for row in rows:
        print('  '.join(f'{str(v):<22}' for v in row))


show('Top 5 best-selling games', '''
    SELECT
        g.title,
        COUNT(*)                          AS sales,
        ROUND(COUNT(*) * g.price, 2)      AS revenue
    FROM purchases p
    JOIN games g ON p.game_id = g.game_id
    GROUP BY g.game_id
    ORDER BY sales DESC
    LIMIT 5
''')

show('Revenue by genre', '''
    SELECT
        g.genre,
        COUNT(*)                AS sales,
        ROUND(SUM(g.price), 2)  AS total_revenue,
        ROUND(AVG(g.price), 2)  AS avg_price
    FROM purchases p
    JOIN games g ON p.game_id = g.game_id
    GROUP BY g.genre
    ORDER BY total_revenue DESC
''')

show('Top 5 customers by spending', '''
    SELECT
        c.name,
        c.country,
        COUNT(*)                AS games_bought,
        ROUND(SUM(g.price), 2)  AS total_spent
    FROM purchases p
    JOIN customers c ON p.customer_id = c.customer_id
    JOIN games g     ON p.game_id     = g.game_id
    GROUP BY c.customer_id
    ORDER BY total_spent DESC
    LIMIT 5
''')

show('Sales by month', '''
    SELECT
        STRFTIME('%Y-%m', purchase_date)  AS month,
        COUNT(*)                          AS sales,
        ROUND(SUM(g.price), 2)            AS revenue
    FROM purchases p
    JOIN games g ON p.game_id = g.game_id
    GROUP BY month
    ORDER BY month
''')

show('Games with no sales', '''
    SELECT g.title, g.genre, g.price
    FROM games g
    LEFT JOIN purchases p ON g.game_id = p.game_id
    WHERE p.purchase_id IS NULL
''')

show('Average customer age by genre', '''
    SELECT
        g.genre,
        ROUND(AVG(c.age), 1)  AS avg_age,
        MIN(c.age)             AS youngest,
        MAX(c.age)             AS oldest
    FROM purchases p
    JOIN games g     ON p.game_id     = g.game_id
    JOIN customers c ON p.customer_id = c.customer_id
    GROUP BY g.genre
    ORDER BY avg_age
''')

show('Customers who spent above average', '''
    SELECT c.name, c.country, ROUND(SUM(g.price), 2) AS total_spent
    FROM purchases p
    JOIN customers c ON p.customer_id = c.customer_id
    JOIN games g     ON p.game_id     = g.game_id
    GROUP BY c.customer_id
    HAVING total_spent > (
        SELECT AVG(total)
        FROM (
            SELECT SUM(g2.price) AS total
            FROM purchases p2
            JOIN games g2 ON p2.game_id = g2.game_id
            GROUP BY p2.customer_id
        )
    )
    ORDER BY total_spent DESC
''')

conn.close()