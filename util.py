import psycopg2
from random import randint


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
    dataTableName = payload['dataTable']
    code = randint(100000, 999999)
    if dataTableName == "credentials":
        existingUser = fetch(dataTableName, {'email': payload['input']['email']})
        if len(existingUser) > 0:
            return {"message": "User already exist"}
        else:
            # payload['input']['isVerified'] = False
            payload['input']['code'] = code
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
        delimiter = []
        for value in values:
            delimiter.append("%s")
        query = '''INSERT INTO {0}'''.format(payload['dataTable'])
        query = query + ''' ('''+" ,".join(parameters) + ") values (" + ",".join(delimiter) + ''') 
        '''
        print("query", query)
        cursor.execute(query, tuple(values))
        isSuccessful = cursor.rowcount
    if isSuccessful and dataTableName == "credentials":
        mailID = payload['input']['email']
        message = '''Hi ''' + mailID + ''',\nGreetings from Next Stay, \nThis is your verification code {0}. \n\n\n Please don't share with others.'''.format(code)
        # message = "This is your verification code" + str(code)
        recipients = [mailID]
        return {"message":message, "recipients":recipients}
    # fields = [field_md[0] for field_md in cursor.description]
    # result = [dict(zip(fields, row)) for row in cursor.fetchall()]
    result = {"executedSuccessfully": isSuccessful}
    print({"executedSuccessfully": isSuccessful})
    conn.commit()
    conn.close()
    return result


def update(payload):
    conn = psycopg2.connect(
        database="d1mcchg8iig4uf", user='qgopasstjgvbtx',
        password='936bcf6d1c2d77bb52cac3b38baef32140407294a03b629c87a473cc5b5aa7d6',
        host='ec2-52-22-136-117.compute-1.amazonaws.com', port='5432'
    )

    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    parameters = payload['input'].keys()
    values = payload['input'].values()
    conditions = payload['query']
    delimiter = []
    for value in values:
        delimiter.append("%s")
    cursor = conn.cursor()
    query = '''Update {0} set '''.format(payload['dataTable'])
    for param in parameters:
        query = query + ''' {0} = '{1}' ,'''.format(param, payload['input'][param])
    query = query[:-1] + "where "
    # query = query + ''' (''' + " ,".join(parameters) + ") values (" + ",".join(delimiter) + ''') '''
    keys = conditions.keys()
    for key in keys:
        query = query + '''{0} = '{1}' AND'''.format(key, conditions[key])
    query = query[:-4]
    print("query", query)
    cursor.execute(query, tuple(values))
    isSuccessful = cursor.rowcount
    result = {"executedSuccessfully": isSuccessful}
    print({"executedSuccessfully": isSuccessful})
    conn.commit()
    conn.close()
    return result
