import sqlite3 as sql
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
                Price INTEGER,
                Quantity INTEGER
    );
        """)
    con.commit()

    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                ID INTEGER PRIMARY KEY,
                buyer_id INTEGER,
                product_id INTEGER,
                amount INTEGER,
                FOREIGN KEY (buyer_id) REFERENCES users(ID),
                FOREIGN KEY (product_id) REFERENCES goods(ID)
    );
        """)
    con.commit()

    # data = {'id': 1, 'name': 'Tim', 'surname': 'Sosnin', 'email': 'tim_sosnin@gmail.com', 'pass': '111111', 'dob': '11.11.1111',
    #         'face': 'https://downloader.disk.yandex.ru/disk/4d77d064cf44808a14da8b851d29f202b687fce56da06602bde6bb80f8753aac/6435ae94/x6m59NaE7ol88Bg7tK2hR7bVlGtc-zjn96Uvws9cyrXsxfvsKI0Mzy3B37Rse4p3ludyYMUkyNOWPbqaVL90SA%3D%3D?uid=1768214715&filename=_tim.sosnin%40gmail.com&disposition=attachment&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=1768214715&fsize=73890&hid=7a25bd8167b22e519a4baf422147c5c4&media_type=executable&tknv=v2&etag=5be1cfd70f7128d8350fce0846adb876'}
    # query = f"INSERT INTO users VALUES ('{data['id']}', '{data['name']}', '{data['surname']}', '{data['email']}', '{data['pass']}', '{data['dob']}', '{data['face']}', {0})"
    # cur = con.cursor()
    # cur.execute(query)
    # con.commit()

    con.close()


if __name__ == '__main__':
    create_DB()
