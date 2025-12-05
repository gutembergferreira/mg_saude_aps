from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import relationship

from ..db.base import Base


class DimTempo(Base):
    __tablename__ = "dim_tempo"
    __table_args__ = {"schema": "dw"}

    id_tempo = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False, unique=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    dia = Column(Integer, nullable=False)
    trimestre = Column(Integer, nullable=False)
    quadrimestre = Column(Integer, nullable=False)
    nome_mes = Column(String(20), nullable=False)
    nome_dia_semana = Column(String(20), nullable=False)
    eh_final_semana = Column(Boolean, nullable=False, server_default=text("false"))

    cadastros = relationship("FatoCadastroAPS", back_populates="tempo")
    atendimentos = relationship("FatoAtendimentoAPS", back_populates="tempo")
    indicadores = relationship("FatoIndicadorAPS", back_populates="tempo")
    financeiros = relationship("FatoFinanceiroAPS", back_populates="tempo")


class DimMunicipio(Base):
    __tablename__ = "dim_municipio"
    __table_args__ = {"schema": "dw"}

    id_municipio = Column(Integer, primary_key=True)
    codigo_ibge = Column(String(7), nullable=False, unique=True)
    nome = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)
    regional_saude = Column(String(100))
    populacao_estim = Column(Integer)

    unidades = relationship("DimUnidadeSaude", back_populates="municipio")
    pacientes = relationship("DimPaciente", back_populates="municipio")
    cadastros = relationship("FatoCadastroAPS", back_populates="municipio")
    atendimentos = relationship("FatoAtendimentoAPS", back_populates="municipio")
    indicadores = relationship("FatoIndicadorAPS", back_populates="municipio")
    financeiros = relationship("FatoFinanceiroAPS", back_populates="municipio")


class DimUnidadeSaude(Base):
    __tablename__ = "dim_unidade_saude"
    __table_args__ = {"schema": "dw"}

    id_unidade = Column(Integer, primary_key=True)
    codigo_cnes = Column(String(15), nullable=False)
    nome = Column(String(150), nullable=False)
    tipo_unidade = Column(String(50))
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=False)

    municipio = relationship("DimMunicipio", back_populates="unidades")
    equipes = relationship("DimEquipe", back_populates="unidade")
    cadastros = relationship("FatoCadastroAPS", back_populates="unidade")
    atendimentos = relationship("FatoAtendimentoAPS", back_populates="unidade")
    indicadores = relationship("FatoIndicadorAPS", back_populates="unidade")


class DimEquipe(Base):
    __tablename__ = "dim_equipe"
    __table_args__ = {"schema": "dw"}

    id_equipe = Column(Integer, primary_key=True)
    codigo_equipe = Column(String(50), nullable=False)
    tipo_equipe = Column(String(50))
    descricao = Column(String(150))
    id_unidade = Column(Integer, ForeignKey("dw.dim_unidade_saude.id_unidade"), nullable=False)

    unidade = relationship("DimUnidadeSaude", back_populates="equipes")
    territorios = relationship("DimTerritorio", back_populates="equipe")
    cadastros = relationship("FatoCadastroAPS", back_populates="equipe")
    atendimentos = relationship("FatoAtendimentoAPS", back_populates="equipe")
    indicadores = relationship("FatoIndicadorAPS", back_populates="equipe")


class DimProfissional(Base):
    __tablename__ = "dim_profissional"
    __table_args__ = {"schema": "dw"}

    id_profissional = Column(Integer, primary_key=True)
    cbo = Column(String(10))
    nome_abreviado = Column(String(100))
    conselho_classe = Column(String(20))
    numero_registro = Column(String(30))

    atendimentos = relationship("FatoAtendimentoAPS", back_populates="profissional")


class DimTerritorio(Base):
    __tablename__ = "dim_territorio"
    __table_args__ = {"schema": "dw"}

    id_territorio = Column(Integer, primary_key=True)
    codigo_territorio = Column(String(50), nullable=False)
    descricao = Column(String(150))
    id_equipe = Column(Integer, ForeignKey("dw.dim_equipe.id_equipe"))

    equipe = relationship("DimEquipe", back_populates="territorios")
    cadastros = relationship("FatoCadastroAPS", back_populates="territorio")
    atendimentos = relationship("FatoAtendimentoAPS", back_populates="territorio")
    indicadores = relationship("FatoIndicadorAPS", back_populates="territorio")


class DimPaciente(Base):
    __tablename__ = "dim_paciente"
    __table_args__ = {"schema": "dw"}

    id_paciente = Column(BigInteger, primary_key=True)
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=False)
    sexo = Column(String(1))
    data_nascimento = Column(Date)
    faixa_etaria = Column(String(20))
    hash_identificador = Column(String(128))

    municipio = relationship("DimMunicipio", back_populates="pacientes")
    cadastros = relationship("FatoCadastroAPS", back_populates="paciente")
    atendimentos = relationship("FatoAtendimentoAPS", back_populates="paciente")


class DimIndicador(Base):
    __tablename__ = "dim_indicador"
    __table_args__ = {"schema": "dw"}

    id_indicador = Column(Integer, primary_key=True)
    codigo = Column(String(20), nullable=False)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    tipo = Column(String(50))
    fonte_metodologia = Column(String(200))

    indicadores = relationship("FatoIndicadorAPS", back_populates="indicador")


class FatoCadastroAPS(Base):
    __tablename__ = "fato_cadastro_aps"
    __table_args__ = {"schema": "dw"}

    id_fato_cad = Column(BigInteger, primary_key=True)
    id_tempo = Column(Integer, ForeignKey("dw.dim_tempo.id_tempo"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=False)
    id_unidade = Column(Integer, ForeignKey("dw.dim_unidade_saude.id_unidade"))
    id_equipe = Column(Integer, ForeignKey("dw.dim_equipe.id_equipe"))
    id_paciente = Column(BigInteger, ForeignKey("dw.dim_paciente.id_paciente"))
    id_territorio = Column(Integer, ForeignKey("dw.dim_territorio.id_territorio"))
    cadastro_valido = Column(Boolean, nullable=False)
    eh_publico_alvo = Column(Boolean, nullable=False)
    peso_capitacao = Column(Numeric(10, 4))

    tempo = relationship("DimTempo", back_populates="cadastros")
    municipio = relationship("DimMunicipio", back_populates="cadastros")
    unidade = relationship("DimUnidadeSaude", back_populates="cadastros")
    equipe = relationship("DimEquipe", back_populates="cadastros")
    paciente = relationship("DimPaciente", back_populates="cadastros")
    territorio = relationship("DimTerritorio", back_populates="cadastros")


class FatoAtendimentoAPS(Base):
    __tablename__ = "fato_atendimento_aps"
    __table_args__ = {"schema": "dw"}

    id_fato_atend = Column(BigInteger, primary_key=True)
    id_tempo = Column(Integer, ForeignKey("dw.dim_tempo.id_tempo"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=False)
    id_unidade = Column(Integer, ForeignKey("dw.dim_unidade_saude.id_unidade"))
    id_equipe = Column(Integer, ForeignKey("dw.dim_equipe.id_equipe"))
    id_profissional = Column(Integer, ForeignKey("dw.dim_profissional.id_profissional"))
    id_paciente = Column(BigInteger, ForeignKey("dw.dim_paciente.id_paciente"))
    id_territorio = Column(Integer, ForeignKey("dw.dim_territorio.id_territorio"))
    tipo_atendimento = Column(String(50))
    codigo_proced = Column(String(20))
    quantidade = Column(Numeric(10, 2), server_default=text("1"))
    local_atendimento = Column(String(50))
    origem_dado = Column(String(50))

    tempo = relationship("DimTempo", back_populates="atendimentos")
    municipio = relationship("DimMunicipio", back_populates="atendimentos")
    unidade = relationship("DimUnidadeSaude", back_populates="atendimentos")
    equipe = relationship("DimEquipe", back_populates="atendimentos")
    profissional = relationship("DimProfissional", back_populates="atendimentos")
    paciente = relationship("DimPaciente", back_populates="atendimentos")
    territorio = relationship("DimTerritorio", back_populates="atendimentos")


class FatoIndicadorAPS(Base):
    __tablename__ = "fato_indicador_aps"
    __table_args__ = {"schema": "dw"}

    id_fato_ind = Column(BigInteger, primary_key=True)
    id_tempo = Column(Integer, ForeignKey("dw.dim_tempo.id_tempo"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=False)
    id_unidade = Column(Integer, ForeignKey("dw.dim_unidade_saude.id_unidade"))
    id_equipe = Column(Integer, ForeignKey("dw.dim_equipe.id_equipe"))
    id_territorio = Column(Integer, ForeignKey("dw.dim_territorio.id_territorio"))
    id_indicador = Column(Integer, ForeignKey("dw.dim_indicador.id_indicador"), nullable=False)
    periodo_referencia = Column(String(10), nullable=False)
    numerador = Column(Numeric(18, 4))
    denominador = Column(Numeric(18, 4))
    valor = Column(Numeric(18, 4))
    meta = Column(Numeric(18, 4))
    atingiu_meta = Column(Boolean)

    tempo = relationship("DimTempo", back_populates="indicadores")
    municipio = relationship("DimMunicipio", back_populates="indicadores")
    unidade = relationship("DimUnidadeSaude", back_populates="indicadores")
    equipe = relationship("DimEquipe", back_populates="indicadores")
    territorio = relationship("DimTerritorio", back_populates="indicadores")
    indicador = relationship("DimIndicador", back_populates="indicadores")


class FatoFinanceiroAPS(Base):
    __tablename__ = "fato_financeiro_aps"
    __table_args__ = {"schema": "dw"}

    id_fato_fin = Column(BigInteger, primary_key=True)
    id_tempo = Column(Integer, ForeignKey("dw.dim_tempo.id_tempo"), nullable=False)
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=False)
    tipo_recurso = Column(String(50))
    programa = Column(String(100))
    valor_creditado = Column(Numeric(18, 2))
    competencia_ref = Column(String(7))
    origem_dado = Column(String(50))

    tempo = relationship("DimTempo", back_populates="financeiros")
    municipio = relationship("DimMunicipio", back_populates="financeiros")
