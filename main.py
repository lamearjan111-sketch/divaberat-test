from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# ----------------------------
# DATABASE
# ----------------------------

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Integer)
    y = Column(Integer)
    # 134.893734 #float


Base.metadata.create_all(bind=engine)

# ----------------------------
# FASTAPI
# ----------------------------

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class PointCreate(BaseModel):
    x: int
    y: int


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.get("/map", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="map.html",
    )


@app.get("/points")
def get_points():
    db = SessionLocal()

    points = db.query(Point).all() # Select * from Points

    result = [
        {
            "id": p.id,
            "x": p.x,
            "y": p.y
        }
        for p in points
    ]

    db.close()

    return result


@app.post("/points")
def add_point(point: PointCreate):
    db = SessionLocal()

    new_point = Point(x=point.x, y=point.y)

    db.add(new_point)
    db.commit()
    db.refresh(new_point)

    db.close()

    return {
        "message": "Point added",
        "point": {
            "id": new_point.id,
            "x": new_point.x,
            "y": new_point.y
        }
    }

