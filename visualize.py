import sqlite3
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DARK_BG   = '#0f1923'
CARD_BG   = '#1a2634'
BORDER    = '#2a3f55'
TEXT      = '#c7d5e0'
ACCENT    = '#66c0f4'
BLUE      = '#1b9edb'
GREEN     = '#4caf50'
ORANGE    = '#ff6b35'
PURPLE    = '#9c6bff'

plt.rcParams.update({
    'figure.facecolor': DARK_BG,
    'axes.facecolor':   CARD_BG,
    'axes.edgecolor':   BORDER,
    'axes.labelcolor':  TEXT,
    'xtick.color':      TEXT,
    'ytick.color':      TEXT,
    'text.color':       TEXT,
    'grid.color':       BORDER,
    'grid.alpha':       0.5,
})

conn = sqlite3.connect('gamestore.db')
cursor = conn.cursor()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Game Store — Sales Dashboard', fontsize=18,
             color=ACCENT, fontweight='bold', y=0.98)


# Revenue by genre
ax = axes[0, 0]
cursor.execute('''
    SELECT g.genre, ROUND(SUM(g.price), 2)
    FROM purchases p JOIN games g ON p.game_id = g.game_id
    GROUP BY g.genre ORDER BY SUM(g.price) DESC
''')
rows = cursor.fetchall()
genres   = [r[0] for r in rows]
revenues = [r[1] for r in rows]
bar_colors = [BLUE, GREEN, ORANGE, PURPLE, '#ff4444']
bars = ax.bar(genres, revenues, color=bar_colors[:len(genres)], edgecolor='none')
ax.set_title('Revenue by Genre', color=ACCENT, fontweight='bold')
ax.set_ylabel('Revenue ($)')
ax.grid(True, axis='y', alpha=0.3)
for bar, val in zip(bars, revenues):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
            f'${val}', ha='center', fontsize=9)


# Top 5 games by sales
ax = axes[0, 1]
cursor.execute('''
    SELECT g.title, COUNT(*) AS sales
    FROM purchases p JOIN games g ON p.game_id = g.game_id
    GROUP BY g.game_id ORDER BY sales DESC LIMIT 5
''')
rows   = cursor.fetchall()
titles = [r[0] for r in rows]
sales  = [r[1] for r in rows]
bars = ax.barh(titles, sales, color=BLUE, edgecolor='none')
ax.set_title('Top 5 Games by Sales', color=ACCENT, fontweight='bold')
ax.set_xlabel('Total Sales')
ax.grid(True, axis='x', alpha=0.3)
for bar, val in zip(bars, sales):
    ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
            str(val), va='center', fontsize=9)


# Monthly sales and revenue
ax = axes[1, 0]
cursor.execute('''
    SELECT STRFTIME('%b', purchase_date), COUNT(*), ROUND(SUM(g.price), 2)
    FROM purchases p JOIN games g ON p.game_id = g.game_id
    GROUP BY STRFTIME('%Y-%m', purchase_date)
    ORDER BY STRFTIME('%Y-%m', purchase_date)
''')
rows    = cursor.fetchall()
months  = [r[0] for r in rows]
m_sales = [r[1] for r in rows]
m_rev   = [r[2] for r in rows]
x = range(len(months))
ax.bar(x, m_rev, color=GREEN, alpha=0.7, edgecolor='none', label='Revenue ($)')
ax2 = ax.twinx()
ax2.plot(x, m_sales, color=ORANGE, marker='o', linewidth=2, markersize=6, label='Sales')
ax.set_xticks(list(x))
ax.set_xticklabels(months)
ax.set_title('Monthly Sales & Revenue', color=ACCENT, fontweight='bold')
ax.set_ylabel('Revenue ($)', color=GREEN)
ax2.set_ylabel('Sales', color=ORANGE)
ax.grid(True, axis='y', alpha=0.3)
legend = [mpatches.Patch(color=GREEN, label='Revenue ($)'),
          mpatches.Patch(color=ORANGE, label='Sales')]
ax.legend(handles=legend, facecolor=CARD_BG, edgecolor=BORDER, loc='upper left')


# Top customers by spending
ax = axes[1, 1]
cursor.execute('''
    SELECT c.name, ROUND(SUM(g.price), 2)
    FROM purchases p
    JOIN customers c ON p.customer_id = c.customer_id
    JOIN games g     ON p.game_id     = g.game_id
    GROUP BY c.customer_id ORDER BY SUM(g.price) DESC LIMIT 5
''')
rows  = cursor.fetchall()
names = [r[0] for r in rows]
spent = [r[1] for r in rows]
colors = [ORANGE if s == max(spent) else BLUE for s in spent]
bars = ax.bar(names, spent, color=colors, edgecolor='none')
ax.set_title('Top 5 Customers by Spending', color=ACCENT, fontweight='bold')
ax.set_ylabel('Total Spent ($)')
ax.grid(True, axis='y', alpha=0.3)
for bar, val in zip(bars, spent):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
            f'${val}', ha='center', fontsize=9)


plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('dashboard.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close()

conn.close()
print('Dashboard saved to dashboard.png')