from pony.orm import Database, Required, Optional, Json

db = Database()
db.bind(provider='sqlite', filename='db.sqlite', create_db=True)


class User(db.Entity):
    user_id = Required(str, unique=True)
    user_city = Optional(str,)


class UserState(db.Entity):
    user_id = Required(str, unique=True)
    scenario_name = Optional(str)
    step_name = Optional(str)
    context = Optional(Json)


db.generate_mapping(create_tables=True)
