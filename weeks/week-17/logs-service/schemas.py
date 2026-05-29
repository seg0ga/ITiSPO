from pydantic import BaseModel


class LogBase(BaseModel):
    message:str
    level:str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id:int

class LogSummary(BaseModel):
    total:int
    by_level:dict[str,int]

class Notification(BaseModel):
    id:int
    log_id:int | str
    message:str
    level:str
    received_at:str

class NotificationAck(BaseModel):
    ok:bool=True
    status:str
    stored:bool=False

class NotificationList(BaseModel):
    ok:bool
    total:int
    notifications:list[Notification]