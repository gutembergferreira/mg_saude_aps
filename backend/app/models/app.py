from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db.base import Base


class Perfil(Base):
    __tablename__ = "app_perfil"

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(Text)

    usuarios = relationship("Usuario", back_populates="perfil")


class Usuario(Base):
    __tablename__ = "app_usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    perfil_id = Column(Integer, ForeignKey("app_perfil.id"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=True)

    perfil = relationship("Perfil", back_populates="usuarios")
    auditorias = relationship("AuditoriaAcesso", back_populates="usuario")


class AuditoriaAcesso(Base):
    __tablename__ = "app_auditoria_acesso"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("app_usuario.id"), nullable=True)
    perfil_nome = Column(String(50))
    endpoint = Column(String(255), nullable=False)
    metodo_http = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_cliente = Column(String(45))
    user_agent = Column(String(255))
    descricao = Column(Text)
    sucesso = Column(Boolean, default=True, nullable=False)

    usuario = relationship("Usuario", back_populates="auditorias")
