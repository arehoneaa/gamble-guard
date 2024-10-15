import sqlite3

# Connect to the database
conn = sqlite3.connect('gambling_sites.db')
cursor = conn.cursor()

# Create the `illegal_sites` table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS illegal_sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE
)
''')

# Create the `legal_sites` table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS legal_sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    name TEXT,
    license TEXT,
    license_expiry DATE
)
''')

# Insert example illegal sites using INSERT OR IGNORE to avoid duplicates
illegal_sites = [
    ('https://illegal-site-1.com',),
    ('https://illegal-site-2.com',),
    ('https://illegal-site-3.com',)
]
cursor.executemany("INSERT OR IGNORE INTO illegal_sites (url) VALUES (?)", illegal_sites)

# Insert example legal sites using INSERT OR IGNORE to avoid duplicates
legal_sites = [
    ('https://www.betway.co.za', 'Betway South Africa', 'ZA123456', '2025-12-31'),
    ('https://www.sunbet.co.za', 'SunBet South Africa', 'ZA654321', '2024-11-30'),
    ('https://www.hollywoodbets.net', 'HollywoodBets', 'ZA789123', '2026-07-15'),
    ('https://www.supabets.co.za', 'Supabets South Africa', 'ZA456789', '2025-09-10'),
    ('https://www.worldsportsbetting.co.za', 'World Sports Betting', 'ZA321654', '2024-08-20'),
    ('https://www.lottostar.co.za', 'LottoStar South Africa', 'ZA852741', '2025-10-05'),
    ('https://www.bettingworld.co.za', 'Betting World', 'ZA963852', '2023-12-31')
]
cursor.executemany("INSERT OR IGNORE INTO legal_sites (url, name, license, license_expiry) VALUES (?, ?, ?, ?)", legal_sites)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")
