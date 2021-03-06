from sqlalchemy import Column, Integer, String,\
    BigInteger, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)


class Zno_subj(Base):
    __tablename__ = 'zno_subj'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):

        return self.name


class Grades(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('Users', backref='grades')
    zno_id = Column(Integer, ForeignKey('zno_subj.id'))
    zno = relationship('Zno_subj', backref='grades')
    grade = Column(Integer)

    def __repr__(self):

        return f'Ваш бал з {self.zno}: {self.grade}'


class Coefficient(Base):
    __tablename__ = 'coefficient'

    id = Column(Integer, primary_key=True)
    zno_id = Column(Integer, ForeignKey('zno_subj.id'))
    zno = relationship('Zno_subj', backref='coefficients')
    speciality_id = Column(Integer, ForeignKey('speciality.id'))
    speciality = relationship('Speciality',backref='coefficients')
    coefficient = Column(Float)
    required = Column(Boolean)

    def __repr__(self):

        return f'ЗНО {self.zno} має коефiцiєнт {self.coefficient}'

class Knowledge_area(Base):
    __tablename__ = 'knowledge_area'

    id = Column(Integer, primary_key=True)
    code = Column(BigInteger)
    name = Column(String(120))

    def __repr__(self):

        return self.name


class Speciality(Base):
    __tablename__ = 'speciality'

    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey('knowledge_area.id'))
    area = relationship('Knowledge_area', backref='specialities')
    name = Column(String(240))
    program = Column(String(120))
    min_rate_budget = Column(Float)
    min_rate_pay = Column(Float)

    def __repr__(self):

        return self.name
