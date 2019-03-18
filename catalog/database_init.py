from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///rifles.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete RifleModelName if exisitng.
session.query(RifleModelName).delete()
# Delete RifleName if exisitng.
session.query(RifleName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="Burri Venkateswarlu",
             email="venkateswarluburri514@gmail.com",
             picture='http://www.enchanting-costarica.com/wp-content/'
                     'uploads/2018/02/jcarvaja17-min.jpg')
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample rifle models
Model1 = RifleModelName(name="Snipers",
                        user_id=1)
session.add(Model1)
session.commit()

Model2 = RifleModelName(name="Assault Rifles",
                        user_id=1)
session.add(Model2)
session.commit

Model3 = RifleModelName(name="SMG",
                        user_id=1)
session.add(Model3)
session.commit()

Model4 = RifleModelName(name="Shotguns",
                        user_id=1)
session.add(Model4)
session.commit()

Model5 = RifleModelName(name="Pistals",
                        user_id=1)
session.add(Model5)
session.commit()

# Rifle details
Name1 = RifleName(name="AWM",
                  ammo=".300",
                  capacity="5",
                  power="100",
                  range="100",
                  stability="34",
                  rlink="https://bit.ly/2O6rV03",
                  date=datetime.datetime.now(),
                  riflemodelnameid=1,
                  user_id=1)
session.add(Name1)
session.commit()

Name2 = RifleName(name="KAR98",
                  ammo="7.62",
                  capacity="5",
                  power="66",
                  range="79",
                  stability="34",
                  rlink="https://bit.ly/2F2UaIU",
                  date=datetime.datetime.now(),
                  riflemodelnameid=1,
                  user_id=1)
session.add(Name2)
session.commit()

Name3 = RifleName(name="M24",
                  ammo="7.62",
                  capacity="5",
                  power="77",
                  range="96",
                  stability="32",
                  rlink="https://bit.ly/2F20Yqa",
                  date=datetime.datetime.now(),
                  riflemodelnameid=1,
                  user_id=1)
session.add(Name3)
session.commit()

Name4 = RifleName(name="M416",
                  ammo="5.56",
                  capacity="30",
                  power="37",
                  range="57",
                  stability="32",
                  rlink="https://bit.ly/2Co1rSO",
                  date=datetime.datetime.now(),
                  riflemodelnameid=2,
                  user_id=1)
session.add(Name4)
session.commit()

Name5 = RifleName(name="AKM",
                  ammo="7.62",
                  capacity="30",
                  power="42",
                  range="60",
                  stability="34",
                  rlink="https://bit.ly/2Cpxl1w",
                  date=datetime.datetime.now(),
                  riflemodelnameid=2,
                  user_id=1)
session.add(Name5)
session.commit()

Name6 = RifleName(name="Scar-l",
                  ammo="5.56",
                  capacity="30",
                  power="37",
                  range="55",
                  stability="31",
                  rlink="https://bit.ly/2u8iOCL",
                  date=datetime.datetime.now(),
                  riflemodelnameid=2,
                  user_id=1)
session.add(Name6)
session.commit()

Name7 = RifleName(name="M16A4",
                  ammo="5.56",
                  capacity="30",
                  power="37",
                  range="62",
                  stability="28",
                  rlink="https://bit.ly/2Hln0aP",
                  date=datetime.datetime.now(),
                  riflemodelnameid=2,
                  user_id=1)
session.add(Name7)
session.commit()

Name8 = RifleName(name="UMP9",
                  ammo="9mm",
                  capacity="30",
                  power="30",
                  range="30",
                  stability="31",
                  rlink="https://bit.ly/2TH8IYP",
                  date=datetime.datetime.now(),
                  riflemodelnameid=3,
                  user_id=1)
session.add(Name8)
session.commit()

Name9 = RifleName(name="Tommy Gun",
                  ammo=".45",
                  capacity="100",
                  power="35",
                  range="46",
                  stability="31",
                  rlink="https://bit.ly/2CpxjGW",
                  date=datetime.datetime.now(),
                  riflemodelnameid=3,
                  user_id=1)
session.add(Name9)
session.commit()

Name10 = RifleName(name="UZI",
                   ammo="9mm",
                   capacity="25",
                   power="21",
                   range="22",
                   stability="31",
                   rlink="https://bit.ly/2XVZ8zz",
                   date=datetime.datetime.now(),
                   riflemodelnameid=3,
                   user_id=1)
session.add(Name10)
session.commit()

Name11 = RifleName(name="M249",
                   ammo="5.56",
                   capacity="100",
                   power="40",
                   range="71",
                   stability="44",
                   rlink="https://bit.ly/2Fed1BP",
                   date=datetime.datetime.now(),
                   riflemodelnameid=3,
                   user_id=1)
session.add(Name11)
session.commit()

Name12 = RifleName(name="S686",
                   ammo="12 G",
                   capacity="2",
                   power="100",
                   range="13",
                   stability="77",
                   rlink="https://bit.ly/2Fe9R14",
                   date=datetime.datetime.now(),
                   riflemodelnameid=4,
                   user_id=1)
session.add(Name12)
session.commit()

Name13 = RifleName(name="S12K",
                   ammo="12 G",
                   capacity="5",
                   power="92",
                   range="9",
                   stability="86",
                   rlink="https://bit.ly/2VYCt3P",
                   date=datetime.datetime.now(),
                   riflemodelnameid=4,
                   user_id=1)
session.add(Name13)
session.commit()

Name14 = RifleName(name="P92",
                   ammo="9mm",
                   capacity="15",
                   power="27",
                   range="15",
                   stability="25",
                   rlink="https://bit.ly/2F21NPM",
                   date=datetime.datetime.now(),
                   riflemodelnameid=5,
                   user_id=1)
session.add(Name14)
session.commit()

Name15 = RifleName(name="P1911",
                   ammo=".45",
                   capacity="7",
                   power="32",
                   range="15",
                   stability="26",
                   rlink="https://bit.ly/2Y1e7bM",
                   date=datetime.datetime.now(),
                   riflemodelnameid=5,
                   user_id=1)
session.add(Name15)
session.commit()

Name16 = RifleName(name="P1895",
                   ammo="7.62",
                   capacity="7",
                   power="42",
                   range="31",
                   stability="29",
                   rlink="https://bit.ly/2ClysiJ",
                   date=datetime.datetime.now(),
                   riflemodelnameid=5,
                   user_id=1)
session.add(Name16)
session.commit()

print("Your rifles database has been inserted!")
