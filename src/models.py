from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from .database import Base


class DataSource(Base):
    __tablename__ = "data_source"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    type = Column(String(32), nullable=False)
    host = Column(String(256))
    port = Column(Integer)
    db_name = Column(String(128))
    username = Column(String(128))
    password_cipher = Column(Text)
    locked = Column(Boolean, nullable=False, default=False)
    status = Column(String(32), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class MetadataTable(Base):
    __tablename__ = "metadata_table"

    id = Column(Integer, primary_key=True, index=True)
    datasource_id = Column(Integer, ForeignKey("data_source.id"), nullable=False)
    schema_name = Column(String(128))
    table_name = Column(String(256), nullable=False)
    chinese_comment = Column(String(512), nullable=False)
    asset_category = Column(String(128), nullable=False)
    security_level = Column(String(32), nullable=False)
    owner_user_id = Column(Integer, nullable=False, default=1)
    table_status = Column(String(32), nullable=False, default="IN_PROGRESS")
    layer_code = Column(String(16), nullable=False)
    ddl_sql = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    datasource = relationship("DataSource")
