from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import *
import os

engine = create_engine(os.environ.get('DATABASE_URL')
                       or 'postgresql://xoxoji:password@localhost/vstup_db')

Base.metadata.create_all(engine)

class DatabaseMapper():

    def __init__(self):

        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def add_area(self, name, code):

        area = self.session.query(Knowledge_area).filter_by(code=code).first()
        if not area:
            area = Knowledge_area(name=name, code=code)
            self.session.add(area)
            self.session.commit()

    def add_speciality(self, spec):

        code = spec['area']
        area = self.session.query(Knowledge_area).filter_by(code=code).first()
        speciality = self.session.query(
            Speciality).filter_by(name=spec['name']).first()

        if not speciality:

            if not spec.get('contract'):
                spec['contract'] = 110

            speciality = Speciality(name=spec['name'], area=area,
                                    program=spec['program'],
                                    min_rate_budget=spec['budget'],
                                    min_rate_pay=spec['contract'])
        self.session.add(speciality)
        self.session.commit()

    def write_coefficients(self, znos, spec):

        speciality = self.session.query(
            Speciality).filter_by(name=spec['name']).first()

        for zno in znos:
            zno_subj = self.session.query(
                Zno_subj).filter_by(name=zno['name']).first()

            if not zno_subj:
                zno_subj = Zno_subj(name=zno['name'])
                self.session.add(zno_subj)

            coef = self.session.query(Coefficient).filter_by(
                zno=zno_subj).filter_by(speciality=speciality).first()
            if not coef:

                coef = Coefficient(zno=zno_subj,
                                   speciality=speciality,
                                   coefficient=zno['coefficient'],
                                   required=zno['required'])
                self.session.add(coef)

            self.session.commit()

    def create_user(self, tg_id):

        user = self.session.query(Users).filter_by(tg_id=tg_id).first()

        if not user:

            user = Users(tg_id=tg_id)

            self.session.add(user)
            self.session.commit()

    def get_grades(self, user):

        grades = self.session.query(Users).filter_by(tg_id=user).first().grades
        return (str(grade) for grade in grades)

    def set_grade(self, user, data):

        user = self.session.query(Users).filter_by(tg_id=user).first()
        zno = self.session.query(Zno_subj).filter_by(name=data['name']).first()
        grade = self.session.query(Grades).filter_by(
            owner_id=user.id, zno=zno).first()

        if not grade:

            if data['grade'] != 0:
                grade = Grades(owner=user, grade=data['grade'], zno=zno)
                self.session.add(grade)
                self.session.commit()
                return 'Оцiнка успiшно додана'
            else:
                return 'У вас ще немає оцiнки з цього предмету.'

        else:
            if data['grade'] == 0:
                self.session.delete(grade)
                self.session.commit()
                return 'Оцiнка успiшно видалена.'
            else:
                grade.grade = data['grade']
                self.session.commit()
                return 'Оцiнка успiшно обновлена.'

    def all_znos(self):

        znos = self.session.query(Zno_subj).all()

        return [str(zno) for zno in znos]

    def all_areas(self):

        areas = self.session.query(Knowledge_area).all()

        return [str(area) for area in areas if area.specialities]

    def specs(self, areaz):

        area = self.session.query(Knowledge_area).filter(
            Knowledge_area.name.startswith(areaz)).first()
        specs = self.session.query(Speciality).filter_by(area=area).all()

        return [str(spec) for spec in specs]

    def grades_for_spec(self, tgid, spec=None, area=None):

        user = self.session.query(Users).filter_by(tg_id=tgid).first()
        if spec:
            speciality = self.session.query(Speciality).filter(
                Speciality.name.startswith(spec)).first()
            coefs = self.session.query(Coefficient).filter_by(
                speciality=speciality)
            grade = self.checking(user, coefs)

            if grade >= speciality.min_rate_budget:

                return 'Вiтаємо! Ви можете поступити на бюджет'
            if grade >= (speciality.min_rate_pay - 10):

                return 'Вiтаємо! Ви можете поступити за контрактом'
            else:

                return 'Нажаль ви не можете поступити за цiєю спецiальнiстю'

        else:
            area = self.session.query(Knowledge_area).filter(
                Knowledge_area.name.startswith(area)).first()
            specs = area.specialities
            budget = []
            contract = []
            for spec in specs:

                coefs = self.session.query(Coefficient).filter_by(
                    speciality=spec)  # getting coefs by query bcs another case we're getting Instrumentallist
                grade = self.checking(user, coefs)

                if grade >= spec.min_rate_budget:
                    budget.append(spec.name)
                if grade >= (spec.min_rate_pay - 10):
                    contract.append(spec.name)

            return {'budget': budget, 'contract': contract}

        '''crutch but idk how to do it another way('''

    def checking(self, user, coefs):

        req_cfs = coefs.filter_by(required=True).all()
        not_req = coefs.filter_by(required=False).all()
        grade = 0
        for req in req_cfs:
            user_grade = self.session.query(Grades).filter_by(
                zno=req.zno, owner=user).first()
            if user_grade:
                grade = grade + user_grade.grade * req.coefficient
            else:
                return 0

        max_third = 0
        for unreq in not_req:
            user_grade = self.session.query(Grades).filter_by(
                zno=unreq.zno, owner=user).first()
            if user_grade:
                if user_grade.grade > max_third:
                    max_third = user_grade.grade

        if max_third == 0:
            return 0

        grade = grade + max_third * not_req[0].coefficient

        return grade
