#!/usr/bin/python3
"""This module is for Database storage"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.city import City
from models import storage_type

if storage_type == 'db':
    from models.place import place_amenity

classes = {"State": State,
           "City": City,
           "User": User,
           "Place": Place,
           "Review": Review,
           "Amenity": Amenity}


class DBStorage:
    """Represents the DBStorage Class
    Class Attributes:
        __engine: the DB engine
        __session: the DB session
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialises the DBStorages instance"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")
        my_engine = 'mysql+mysqldb://{}:{}@{}/{}'
        self.__engine = create_engine(my_engine.format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session all
        objects depending on the giving class name
        """
        o_dict = {}
        if cls is None:
            for classe in classes.values():
                for obj in self.__session.query(classe).all():
                    obj_key = f"{obj.__class__.__name__}.{obj.id}"
                    o_dict[obj_key] = obj
        else:
            for obj in self.__session.query(cls).all():
                obj_key = f"{obj.__class__.__name__}.{obj.id}"
                o_dict[obj_key] = obj
        return o_dict

    def new(self, obj):
        """add the object to the current database session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                    type(obj).id == obj.id).delete()

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove methode on the private session attribute"""
        self.__session.close()
