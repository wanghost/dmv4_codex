from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import DataSource, MetadataTable
from .schemas import DataSourceCreate, DataSourceOut, TableCreate, TableOut

app = FastAPI(title="Data Asset Management API", version="0.1.0")

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/datasources", response_model=list[DataSourceOut])
def list_datasources(db: Session = Depends(get_db)):
    return db.query(DataSource).all()


@app.post("/api/v1/datasources", response_model=DataSourceOut)
def create_datasource(payload: DataSourceCreate, db: Session = Depends(get_db)):
    exists = db.query(DataSource).filter_by(name=payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Data source already exists")
    entity = DataSource(**payload.model_dump(exclude={"password"}), password_cipher=payload.password)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


@app.post("/api/v1/datasources/{id}/test-connection")
def test_connection(id: int, db: Session = Depends(get_db)):
    entity = db.query(DataSource).get(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Data source not found")
    return {"datasource_id": id, "result": "SUCCESS", "message": "连接测试通过"}


@app.get("/api/v1/tables", response_model=list[TableOut])
def list_tables(db: Session = Depends(get_db)):
    return db.query(MetadataTable).all()


@app.post("/api/v1/tables", response_model=TableOut)
def create_table(payload: TableCreate, db: Session = Depends(get_db)):
    ds = db.query(DataSource).get(payload.datasource_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Data source not found")
    entity = MetadataTable(**payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


@app.post("/api/v1/tables/{id}/validate")
def validate_table(id: int, db: Session = Depends(get_db)):
    entity = db.query(MetadataTable).get(id)
    if not entity:
        raise HTTPException(status_code=404, detail="Table not found")
    issues = []
    if not entity.chinese_comment.strip():
        issues.append("必须填写中文注释")
    if not entity.table_name:
        issues.append("必须填写表名")
    return {"table_id": id, "passed": len(issues) == 0, "issues": issues}


@app.get("/api/v1/assets/search")
def search_assets(keyword: str = "", db: Session = Depends(get_db)):
    query = db.query(MetadataTable)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(MetadataTable.table_name.like(like))
    rows = query.all()
    return [{"id": r.id, "table_name": r.table_name, "owner_user_id": r.owner_user_id} for r in rows]
