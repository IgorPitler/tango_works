# pip install --pre mariadb

import mariadb

try:
    conn = mariadb.connect(
        user="tango",
        password="tango",
        host="127.0.0.1",
        port=3306,
        database="tango"
    )
    print("Success: Connected to MariaDB!")

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")

# Get a cursor object to execute queries
cursor = conn.cursor()

try:
    # create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            test_value VARCHAR(50),
            test_value2 VARCHAR(50)
        )
    """)

    # обязательно conn.commit() !
    conn.commit()
    print("Success: Table created")

    # query template
    insert_query = "INSERT INTO test1 (test_value, test_value2) VALUES (?,?)"

    insert_data = ("data1", "data1_1")
    cursor.execute(insert_query, insert_data)
    conn.commit()
    print("record inserted")


    insert_data = ("data2", "data2_1")
    cursor.execute(insert_query, insert_data)
    conn.commit()
    print("record inserted")

    # single field
    query = "SELECT test_value FROM test1 WHERE id = ?"
    id = 1
    # tuple of 1 item!
    cursor.execute(query, (id,))
    row=cursor.fetchone()
    print(f"single field query: {row[0]}")

    select_query = "SELECT id, test_value, test_value2 FROM test1"
    cursor.execute(select_query)
    print("\nQuery Results:")
    for (id, test_value, test_value2) in cursor:
        print(f"id: {id} | test_value: {id} {test_value} {test_value2}")

    # drop table
    cursor.execute("drop table test1")
    conn.commit()
    print("Success: Table dropped")

except mariadb.Error as e:
    print(f"Database error occurred: {e}")
    # Roll back changes if something went wrong during transaction
    #conn.rollback() // last commit?
finally:
    # обязательно все закрыть!
    cursor.close()
    conn.close()
    print("\nConnection closed safely.")