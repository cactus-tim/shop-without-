def create_DB():
    con = sql.connect('../third.db')

    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY,
                Name STRING,
                Surname STRING,
                Email STRING,
                Password STRING,
                Date_of_birth STRING,
                Face STRING,
                Balance INTEGER
    );
        """)
    con.commit()

    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS goods (
                ID INTEGER PRIMARY KEY,
                Name STRING,
                Manufacturer STRING,
                Price INTEGER
    );
        """)
    con.commit()

    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS sales02 (
                ID INTEGER PRIMARY KEY,
                buyer_id INTEGER,
                product_id INTEGER,
                amount INTEGER,
                FOREIGN KEY (buyer_id) REFERENCES users(ID),
                FOREIGN KEY (product_id) REFERENCES goods(ID)
    );
        """)
    con.commit()

    con.close()


if __name__ == '__mian__':
    import sqlite3 as sql

    create_DB()
