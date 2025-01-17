from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class HomeworkImage(Base):
    __tablename__ = "homework_submission"

    id = Column(Integer, primary_key=True)
    image = Column()
    homeworkId = Column()

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")