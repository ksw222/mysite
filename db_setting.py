from database import MyDB

# MyDB class 생성
mydb = MyDB(
    _host = 'hanksw22.mysql.pythonanywhere-services.com',
    _port = 3306,
    _user = 'hanksw22',
    _pw = 'kim0369*',
    _db_name = 'hanksw22$default'
)


# table 생성 쿼리문
create_user = """
    create table
    if not exists
    user (
    id varchar(32) primary key,
    password varchar(64) not null,
    name varchar(32)
    )
"""

mydb.sql_query(create_user)
mydb.commit_db()