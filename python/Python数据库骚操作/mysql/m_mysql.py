
from sqlalchemy import create_engine, Column, Integer, String, BIGINT, ForeignKey, UniqueConstraint, Index, and_, or_, inspect
from sqlalchemy.orm import sessionmaker, relationship,contains_eager
# echo 为 True 将会打印 SQL 原生语句
engine = create_engine('mysql+pymysql://username:password@localhost:3306/db_name',echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


new_user = Users(name='zone', age=18)
session.add(new_user)
# 批量添加
session.add_all([
    User(name='zone2', age=25),
    User(name='zone3', age=32)
])
# 提交
session.commit()

session.query(User).filter_by(name="zone").delete()
# 提交
session.commit()

session.query(User).filter(User.name == 2).update({"name": "new name"})
session.query(User).filter(User.id >= 3).update({User.name: "关注公众号【zone7】"}, synchronize_session=False)
session.query(User).filter(User.age == 50).update({"age": 123}, synchronize_session="evaluate")
session.commit()


result = session.query(User).all()   # 结果为一个列表
result = session.query(User.id, User.age).all()
result = session.query(User).filter_by(name='zone').first()
result = session.query(User).filter_by(name='zone2').all()
# 与、或
result = session.query(User).filter_by(and_(name='zone5',age="23")).all()
result = session.query(User).filter_by(or_(name='zone5',age="23")).all()
# 模糊查询
result = session.query(User).filter(User.name.like('zon%')).all()
# 排序
result = session.query(User).order_by(User.age.desc()).all()
# 分页查询
result = session.query(User).offset(1).limit(1).all()