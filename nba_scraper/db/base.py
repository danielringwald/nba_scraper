from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """
    MappedAsDataclass turns DB models into Python native dataclasses meaning:
    * We get automatic __init__, __repr__

    The One Big Catch: default vs. insert_default
    Because MappedAsDataclass maps directly to Python's native dataclasses, the keyword argument name default gets taken over by Python to mean "the default value when I create this object in Python".

    If you want to set a database-level default value (the value Postgres inserts if the column is empty), you have to use insert_default instead:
    """
    pass