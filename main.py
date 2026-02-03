from sqlalchemy import create_engine, String, Integer, select, func, update, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session



engine = create_engine("sqlite:///school.db")


class Base(DeclarativeBase):
    pass


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    experience: Mapped[int] = mapped_column(Integer, nullable=False)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# 1-BOSQICH: INSERT + SELECT

with Session(engine) as session:
    session.add_all([
        Teacher(name="Anvar", subject="Matematika", experience=5),
        Teacher(name="Nilufar", subject="Fizika", experience=8),
        Teacher(name="Rustam", subject="Kimyo", experience=3),
    ])
    session.commit()

    print("\nBarcha teacherlar:")
    for t in session.scalars(select(Teacher)):
        print(t.id, t.name, t.subject, t.experience)

    print("\nSubject = Fizika:")
    print(session.scalars(
        select(Teacher).where(Teacher.subject == "Fizika")
    ).first())

    print("\nExperience >= 5:")
    for t in session.scalars(
        select(Teacher).where(Teacher.experience >= 5)
    ):
        print(t.name)

    print("\nFaqat name va subject:")
    for row in session.execute(
        select(Teacher.name, Teacher.subject)
    ):
        print(row)

    print("\nID = 2:")
    print(session.get(Teacher, 2))

    print("\nExperience desc:")
    for t in session.scalars(
        select(Teacher).order_by(Teacher.experience.desc())
    ):
        print(t.name, t.experience)

    print("\nTeacherlar soni:")
    print(session.scalar(select(func.count(Teacher.id))))

    print("\nSubject = Kimyo:")
    print(session.scalars(
        select(Teacher).where(Teacher.subject == "Kimyo")
    ).all())


# 2-BOSQICH: UPDATE

with Session(engine) as session:
    session.execute(
        update(Teacher).where(Teacher.name == "Anvar")
        .values(experience=6)
    )

    session.execute(
        update(Teacher).where(Teacher.id == 3)
        .values(subject="Biologiya")
    )

    session.execute(
        update(Teacher).where(Teacher.experience < 5)
        .values(subject="Informatika")
    )

    session.execute(
        update(Teacher).where(Teacher.name == "Nilufar")
        .values(experience=10)
    )

    t1 = session.get(Teacher, 1)
    t1.name = "Anvarbek"
    t1.experience = 7

    session.execute(
        update(Teacher).where(Teacher.experience >= 8)
        .values(subject="Fizika-Advanced")
    )

    session.execute(
        update(Teacher).where(Teacher.id == 2)
        .values(name="")
    )

    session.commit()

    print("\nUPDATE dan keyin:")
    for t in session.scalars(select(Teacher)):
        print(t.id, t.name, t.subject, t.experience)


# 3-BOSQICH: DELETE

with Session(engine) as session:
    session.execute(delete(Teacher).where(Teacher.id == 1))
    session.execute(delete(Teacher).where(Teacher.experience < 5))
    session.execute(delete(Teacher).where(Teacher.subject == "Fizika"))
    session.execute(delete(Teacher))
    session.execute(delete(Teacher).where(Teacher.experience >= 7))

    session.commit()

    print("\nDELETE dan keyin:")
    print(session.scalars(select(Teacher)).all())


