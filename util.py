import psycopg2


def fetch():
    # establishing the connection
    conn = psycopg2.connect(
        database="d1mcchg8iig4uf", user='qgopasstjgvbtx',
        password='936bcf6d1c2d77bb52cac3b38baef32140407294a03b629c87a473cc5b5aa7d6',
        host='ec2-52-22-136-117.compute-1.amazonaws.com', port='5432'
    )

    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute('''SELECT * from STAYS''')
    fields = [field_md[0] for field_md in cursor.description]
    result = [dict(zip(fields, row)) for row in cursor.fetchall()]
    # result = cursor.fetchall()
    print(result)
    conn.commit()
    conn.close()
    return result
