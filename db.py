from os import environ

import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()

clients = sqlalchemy.Table(
    "clients",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("document", sqlalchemy.String(300), nullable=False),
    sqlalchemy.Column("surname", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("patronymic", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False),
)

pets = sqlalchemy.Table(
    "pets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("client_id", sqlalchemy.ForeignKey("clients.id"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False),
)

consultations = sqlalchemy.Table(
    "consultations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("client_id", sqlalchemy.ForeignKey("clients.id"), nullable=False),
    sqlalchemy.Column("pet_id", sqlalchemy.ForeignKey("pets.id"), nullable=False),
    sqlalchemy.Column("date_time", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(300), nullable=True),
)


TESTING = environ.get("TESTING")

if TESTING:
    TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
    database = databases.Database(TEST_SQLALCHEMY_DATABASE_URL)
    engine = sqlalchemy.create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///mydatabase.db"
    database = databases.Database(SQLALCHEMY_DATABASE_URL)
    engine = sqlalchemy.create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

metadata.create_all(engine)
