import psycopg2


def fetch(dataTable, input):
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
    query = '''SELECT * from {0}'''.format(dataTable)
    if input != None :
        parameters=input.keys()
        query = query + ''' where'''
        for param in parameters:
            query= query + ''' {0} = '{1}' AND'''.format(param,input[param])
        query = query[:-4]
    print("query",query)
    cursor.execute(query)
    fields = [field_md[0] for field_md in cursor.description]
    result = [dict(zip(fields, row)) for row in cursor.fetchall()]
    # result = cursor.fetchall()
    print(result)
    conn.commit()
    conn.close()
    return result

def create(payload):
    conn = psycopg2.connect(
        database="d1mcchg8iig4uf", user='qgopasstjgvbtx',
        password='936bcf6d1c2d77bb52cac3b38baef32140407294a03b629c87a473cc5b5aa7d6',
        host='ec2-52-22-136-117.compute-1.amazonaws.com', port='5432'
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    isSuccessful = 0
    if payload != None:
        parameters = list(payload['input'].keys())
        values = payload['input'].values()
        query = '''INSERT INTO {0}'''.format(payload['dataTable'])
        query = query + ''' ('''+" ,".join(parameters) + " ) values ( '" + "' ,'".join(values) + ''' ')'''
        print("query", query)
        isSuccessful = cursor.execute(query)
    # fields = [field_md[0] for field_md in cursor.description]
    # result = [dict(zip(fields, row)) for row in cursor.fetchall()]
    result = {"executedSuccessfully": isSuccessful}
    print({"executedSuccessfully": isSuccessful})
    conn.commit()
    conn.close()
    return result
