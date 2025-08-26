from helpers.database import db
from marshmallow import Schema, fields, validate
from sqlalchemy import PrimaryKeyConstraint, BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Instituicao(db.Model):
    __tablename__ = 'instituicoes'
    
   
    NO_REGIAO: Mapped[str] = mapped_column(String)
    CO_REGIAO: Mapped[int] = mapped_column(Integer)
    NO_UF: Mapped[str] = mapped_column(String)
    SG_UF: Mapped[str] = mapped_column(String)
    CO_UF: Mapped[int] = mapped_column(Integer)
    NO_MUNICIPIO: Mapped[str] = mapped_column(String)
    CO_MUNICIPIO: Mapped[int] = mapped_column(Integer)
    NO_MESORREGIAO: Mapped[str] = mapped_column(String)
    NO_MICRORREGIAO: Mapped[str] = mapped_column(String)
    NO_ENTIDADE: Mapped[str] = mapped_column(String)
    CO_ENTIDADE: Mapped[int] = mapped_column(BigInteger)
    QT_MAT_BAS: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_INF: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_FUND: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_MED: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_EJA: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_EJA_FUND: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_ESP: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_BAS_EAD: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_FUND_INT: Mapped[int] = mapped_column(Integer, nullable=True)
    QT_MAT_MED_INT: Mapped[int] = mapped_column(Integer, nullable=True)
    ano: Mapped[int] = mapped_column(Integer)

    __table_args__ = (PrimaryKeyConstraint('CO_ENTIDADE', 'ano'), {})

    def __repr__(self):
        return f'<Instituicao {self.NO_ENTIDADE}>'

class InstituicaoSchema(Schema):
    CO_ENTIDADE = fields.Int(required=True)
    NO_ENTIDADE = fields.Str(required=True, validate=validate.Length(min=3))
    NO_MUNICIPIO = fields.Str(required=True)
    CO_UF = fields.Int(required=True)
    NO_UF = fields.Str(required=True)
    SG_UF = fields.Str(required=True, validate=validate.Length(equal=2))
    QT_MAT_INF = fields.Int(required=False, load_default=0)
    QT_MAT_FUND = fields.Int(required=False, load_default=0)
    ano = fields.Int(required=True)