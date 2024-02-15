from sqlalchemy import Column, DateTime, ForeignKey, Integer, Boolean, Text

from app.core.db import Base


class Donation(Base):
    create_date = Column(DateTime)
    close_date = Column(DateTime)
    # Столбец с внешним ключом: ссылка на таблицу meetingroom.
    charity_project_id = Column(Integer, ForeignKey('charityproject.id'))
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.id',
                                         name='fk_donation_user_id_user'),)

    #def __repr__(self):
     #   return (
      #      f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
       # )
