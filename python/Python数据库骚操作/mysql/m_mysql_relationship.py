from sqlalchemy import create_engine, Column, Integer, String, BIGINT, ForeignKey, UniqueConstraint, Index, and_, or_, \
    inspect, Table
from sqlalchemy.orm import sessionmaker, relationship, contains_eager, joinedload

# echo 为 True 将会输出 SQL 原生语句
engine = create_engine('mysql+pymysql://username:password@local:3306/zone', echo=True)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def object_as_dict(obj):
    result = {}
    for c in inspect(obj).mapper.column_attrs:
        # print(type(getattr(obj, c.key)))
        result[c.key] = getattr(obj, c.key)
    return result


# 初始化数据库
def init_db():
    Base.metadata.create_all(engine)


# 删除数据库
def drop_db():
    Base.metadata.drop_all(engine)


# drop_db()
# init_db()

Session = sessionmaker(bind=engine)
session = Session()


def one_to_one():
    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child = relationship("Child", uselist=False, back_populates="parent")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))
        parent = relationship("Parent", back_populates="child")
        name = Column(String(32))

    # 清空数据库，并且重新初始化
    drop_db()
    init_db()
    child = Child(name="zone")
    parent = Parent(child=child)
    session.add(parent)
    session.commit()

    result = session.query(Parent).join(Child).first()
    print(object_as_dict(result.child))

one_to_one()


def one_to_many():
    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        children = relationship("Child", back_populates="parent")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        name = Column(String(32))
        parent_id = Column(Integer, ForeignKey('parent.id'))
        parent = relationship("Parent", back_populates="children")

        # 子表类中附加一个 relationship() 方法
        # 并且在(父)子表类的 relationship() 方法中使用 relationship.back_populates 参数

    # 清空数据库，并且重新初始化
    drop_db()
    init_db()

    child1 = Child(name="zone1")
    child2 = Child(name="zone2")
    parent = Parent(children=[child1, child2])
    session.add(parent)
    session.commit()
    result = session.query(Parent).join(Child).first()
    print(object_as_dict(result.children[0]))

# one_to_many()

def many_to_many():
    association_table = Table('association', Base.metadata,
                              Column('left_id', Integer, ForeignKey('left.id')),
                              Column('right_id', Integer, ForeignKey('right.id'))
                              )

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True,autoincrement=True)
        children = relationship(
            "Child",
            secondary=association_table,
            back_populates="parents")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True,autoincrement=True)
        name = Column(String(32))
        parents = relationship(
            "Parent",
            secondary=association_table,
            back_populates="children")

    # 清空数据库，并且重新初始化
    drop_db()
    init_db()

    child1 = Child(name="zone1")
    child2 = Child(name="zone2")
    child3 = Child(name="zone3")

    parent = Parent()
    parent2 = Parent()
    # parent 添加 child
    parent.children.append(child1)
    parent.children.append(child2)
    parent2.children.append(child1)
    parent2.children.append(child2)
    # save
    session.add(parent)
    session.add(parent2)
    session.commit()
    # 查询
    result = session.query(Parent).first()
    print(object_as_dict(result))
    print(object_as_dict(result.children[1]))
    result2 = session.query(Child).first()
    print(object_as_dict(result2))
    print(object_as_dict(result2.parents[1]))

# many_to_many()