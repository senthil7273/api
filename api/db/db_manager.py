from ast import Delete
import sqlite3
from typing import Any, ClassVar
from xmlrpc.client import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc as AlchemyException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy import ForeignKey, Float, Integer, DATETIME, delete, update
from sqlalchemy.orm import declarative_base, sessionmaker,Session, scoped_session
import sqlalchemy as sa
from sqlalchemy.sql import func , exists

Base = declarative_base()

class Constant(object):
    TABLE_SENSORS = "sensors"
    TABLE_METRICS = "metrics"
    DB_PATH = "sqlite:///test.db?check_same_thread=False"

class Sensor(Base):
    __tablename__ = Constant.TABLE_SENSORS

    id = Column(Integer, primary_key=True, nullable=False)
    city = Column(String)
    country = Column(String)
     
    def __repr__(self):
        return "<Sensor(id='%s', city='%s', country='%s')>" % (self.id, self.city, self.country)

class Metric(Base):
    __tablename__ = Constant.TABLE_METRICS

    sno = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, ForeignKey(Sensor.id), nullable=False)
    timestamp = Column(DATETIME, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)

    def __repr__(self):
        return "<Metrics (sno='%s', id='%s', timestamp='%s', temperature='%s', humidity='%s')>" % (self.sno, self.id, self.timestamp, self.temperature, self.humidity)


class DBManager(object):

    def __init__(self):
        self._engine = create_engine(Constant.DB_PATH, echo=True)
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)
        self._session = Session()
        
    
    @property
    def session(self) -> sessionmaker:
        return self._session

    @property
    def engine(self) -> Any:
        print(" *****  ")
        Debugger.table_exists(self._engine, 'sensors')
        Debugger.table_exists(self._engine, 'metrics')
        return self._engine



class DataProcessor:
    
    def delete_all(self, session, obj):
        count = session.query(obj).filter(obj.id != None).delete(synchronize_session=False)
        session.commit()
        return count

    def delete(self, session, obj, id=None):
        count = session.query(obj).filter(obj.id == id).delete(synchronize_session=False)
        session.commit()
        return count
    
    def add(self, session, obj):
        try:
            if isinstance(obj, list):
                session.add_all(obj)
            else:
                session.add(obj)
            session.commit()
        except AlchemyException.IntegrityError as err:
            session.rollback()
            raise DuplicateError()
        except Exception as exp:
            session.rollback()
            raise UnkownError()

    def add_by(self, session, obj):
        try:
            if isinstance(obj, list):
                session.add_all(obj)
            else:
                print("coming here 1")
                record = session.query(Sensor).filter(obj.id == Sensor.id).first()
                print("coming here 2")
                
                if record is not None:
                    print("coming here 3")
                    session.add(obj)
                    session.commit()
                else:
                    print("coming here 4")        
                    raise UnknownSensorError()
        except AlchemyException.IntegrityError as err:
            session.rollback()
            raise DuplicateError()
        except UnknownSensorError as exp:
            print("coming here 5")
            raise UnknownSensorError()
        except Exception as exp:
            print("coming here 6")
            session.rollback()
            raise UnkownError()

    def get_all(self, session, obj):
        records = session.query(obj).all()
        return records

    def get_by_id(self, session, obj, id=None):
        record = session.query(obj).filter(obj.id == id).first()
        return record

    def get_by_id_all(self, session, obj, id=None):
        record = session.query(obj).filter(obj.id == id).all()
        return record

    def get_average(self, session, obj):
        avg = session.query \
                    (func.avg(obj.temperature).label('avg_temp'), \
                    func.avg(obj.humidity).label('avg_humidity'))
        average = avg.all() 
        result = None
        for row in average:
            result = dict(row) 
        return result

    def get_metrics_by_date(self, session, obj, feature):
        if 'start_date' in feature:
            records = session.query(obj).filter(obj.timestamp >= feature['start_date'])
        else:
            records = session.query(obj).all()
        return records


class Debugger(object):
    @classmethod
    def table_exists(self, engine, name):
        ins = sa.inspect(engine)
        result = ins.dialect.has_table(engine.connect(), name)
        print('Table "{}" exists: {}'.format(name, result))
        return result

class Message(object):
   
    MSG_SUCCESS = {"message": "succeed"}
    MSG_FAILED = "failed"
    MSG_NOT_REQUIRED = "method not required"
    MSG_DUPLICATE_SENSOR = "duplicate sensor found" 
    MSG_INTEGRITY_ERROR = "duplicate sensor or missing k/v pairs"
    MSG_UNKOWN_ERROR = "Unknown error"
    MSG_NO_RECORD_FOUND = "no record found"
    MSG_UNKOWN_SENSOR = "Unknown sensor found"

class DuplicateError(Exception):
  
   def __init__(self):
      self.message = Message.MSG_INTEGRITY_ERROR
  
   def __str__(self):
      return(repr(self.value))

class UnkownError(Exception):
  
   def __init__(self):
      self.message = Message.MSG_UNKOWN_ERROR
  
   def __str__(self):
      return(repr(self.value))

class UnknownSensorError(Exception):
  
   def __init__(self):
      self.message = Message.MSG_UNKOWN_SENSOR
  
   def __str__(self):
      return(repr(self.value))
