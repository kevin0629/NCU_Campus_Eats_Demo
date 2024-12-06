from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from flask import current_app
from app import db

# SessionLocal = sessionmaker(bind=db.engine)  # 確保與資料庫引擎綁定

# 創建一個上下文管理器來自動管理 Session 的生命週期
@contextmanager
def get_session():
    session = db.session
    try:
        yield session
        session.commit() # 若有任何變更需要提交
    except Exception:
        session.rollback() # 發生錯誤時回滾事務
        raise
    finally:
        session.close() # 結束後關閉 session