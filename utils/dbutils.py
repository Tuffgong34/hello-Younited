
import utils.dbdetails as dbdetails

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

global_db_details = None
global_con = None
global_meta = None
global_db_session = None
global_base = None

def get_db_details():
    global global_db_details
    if global_db_details is None:
        global_db_details = dbdetails.DBDetails()
    return global_db_details

def get_conn_str():
    db = get_db_details()
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(db.DB_USER, db.DB_PASS, db.DB_HOST, db.DB_PORT, db.DB_NAME)
    return url

def get_base():
    global global_base

    if global_base is None:
        get_db_session()

    return global_base

def get_db_session():
    global global_db_session
    global global_base 

    if global_db_session is None:
        conn_str = get_conn_str()
        engine = create_engine(conn_str, convert_unicode=True)
        global_db_session = scoped_session(sessionmaker(autocommit=False,
                                                autoflush=False,
                                                bind=engine))
        global_base = declarative_base()
        global_base.query = global_db_session.query_property()
    
    return global_db_session

