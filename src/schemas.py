from pydantic import BaseModel, Field


class DataSourceBase(BaseModel):
    name: str
    type: str
    host: str | None = None
    port: int | None = None
    db_name: str | None = None
    username: str | None = None


class DataSourceCreate(DataSourceBase):
    password: str | None = None


class DataSourceOut(DataSourceBase):
    id: int
    locked: bool
    status: str

    class Config:
        from_attributes = True


class TableCreate(BaseModel):
    datasource_id: int
    schema_name: str | None = None
    table_name: str
    chinese_comment: str = Field(min_length=1)
    asset_category: str
    security_level: str
    layer_code: str
    ddl_sql: str | None = None


class TableOut(TableCreate):
    id: int
    table_status: str

    class Config:
        from_attributes = True
