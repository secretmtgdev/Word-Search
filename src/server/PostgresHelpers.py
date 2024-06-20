import psycopg2

import Contsants;

connection = psycopg2.connect(database='ShareDrive', host='localhost', port='5432')
def dbContainsFile(fileName):
    db_contains_file = False
    try:
        with connection.cursor() as cur:
            print(f'CHECKING IF {fileName} EXISTS IN DB')
            cur.execute(Contsants.GET_FILE_BY_NAME, (fileName,))
            file_exists = cur.fetchone()
            print(f'RECORD RETURNED {file_exists}')
            if file_exists is not None:
                db_contains_file = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # there was an issue here, assume there is an entry
        return db_contains_file

def insertFile(fileName):
    file_id = None

    try:
        with connection.cursor() as cur:            
            if not dbContainsFile(fileName=fileName):
                cur.execute(Contsants.ADD_FILE, (fileName,))
                connection.commit()
            else:
                print('FILE ALREADY IN DB')
                return None

    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR WHEN CONNECTING WITH DB')
        print(error)
    finally:
        return file_id

def getAllFiles():
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT file_name FROM files;")
            records = cur.fetchall()
            return [fileName[0] for fileName in records]
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR WHEN CONNECTING WITH DB')
        print(error)

def uploadToDataStore(file_to_upload):
    BLOB = psycopg2.Binary(file_to_upload.read())
    try:
        with connection.cursor() as cur:
            cur.execute("INSERT INTO file_datastore(file_name, blob, file_size) VALUES(%s, %s, %s)", (file_to_upload.filename, BLOB, file_to_upload.__sizeof__()))       
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR WHEN UPLOADING BLOB')
        print(error)
    finally:
        if connection is not None:
            connection.commit()
    
def getFileFromDataStore(fileName):
    print('GETTING FILE FROM BLOB STOAGE')
    try:
        with connection.cursor() as cur:
            cur.execute(Contsants.GET_BLOB_BY_FILE_NAME, (fileName,))
            record = cur.fetchone()
            return {
                'blobData': bytes(record[0]).decode()
            }
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(f'ERROR WHEN FETCHING {fileName} FROM BLOB STORAGE')
        print(error)
    finally:
        if connection is not None:
            connection.commit()

def deleteFromDataStore(fileName):
    try:
        with connection.cursor() as cur:
            cur.execute(Contsants.DELETE_FILE_BY_NAME, (fileName, ))
            cur.execute(Contsants.DELETE_BLOB_BY_FILE_NAME, (fileName, ))
            cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print('ERROR WHEN DELETING {fileName} FROM TABLES')
        print(error)
    finally:
        if connection is not None:
            connection.commit()
    