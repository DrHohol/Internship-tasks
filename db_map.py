from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import *

engine = create_engine('postgresql:///vstup_db')

#Session = sessionmaker(bind=engine)
#session = Session()

Base.metadata.create_all(engine)

class DatabaseMapper():

    def __init__(self):

        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()


    def add_area(self,name,code):

        area = self.session.query(Knowledge_area).filter_by(code=code).first()
        if not area:
            area = Knowledge_area(name=name,code=code)
            self.session.add(area)
            self.session.commit()


    def add_speciality(self,spec):

        code = spec['area']
        area = self.session.query(Knowledge_area).filter_by(code=code).first()
        speciality = self.session.query(Speciality).filter_by(name=spec['name']).first()
        
        if not speciality:

            if not spec.get('contract'):
                spec['contract'] = 110

            speciality = Speciality(name=spec['name'],area=area,
                                    program=spec['program'],min_rate_budget=spec['budget'],
                                    min_rate_pay=spec['contract'])
        self.session.add(speciality)
        self.session.commit()
    
    def write_coefficients(self,znos,spec):

        speciality = self.session.query(Speciality).filter_by(name=spec['name']).first()

        for zno in znos:
            zno_subj = self.session.query(Zno_subj).filter_by(name=zno['name']).first()

            if not zno_subj:
                zno_subj = Zno_subj(name=zno['name'])
                self.session.add(zno_subj)

            coef = self.session.query(Coefficient).filter_by(zno=zno_subj).filter_by(speciality=speciality).first()
            if not coef:

                coef = Coefficient(zno=zno_subj,
                    speciality=speciality,coefficient=zno['coefficient'],
                    required=zno['required'])
                self.session.add(coef)

            self.session.commit()

    def create_user(self,tg_id):

        user = self.session.query(Users).filter_by(tg_id=tg_id).first()

        if not user:

            user = Users(tg_id=tg_id)

            self.session.add(user)
            self.session.commit()

    def get_grades(self,user):

        grades = self.session.query(Users).filter_by(tg_id=user).first().grades
        return (str(grade) for grade in grades)

    def set_grade(self,user,data):

        user = self.session.query(Users).filter_by(tg_id=user).first()
        zno = self.session.query(Zno_subj).filter_by(name=data).first()
        grade = self.session.query(Grades).filter(owner=user,zno_subj=zno).first()
        if not grade:
            grade = Grades(owner=user,grade=data['grade'],zno=zno)
            self.session.add(grade)
        else:
            grade.grade = data['grade']
        self.session.commit()

    def all_znos(self):

        znos = self.session.query(Zno_subj).all()

        return [str(zno) for zno in znos]