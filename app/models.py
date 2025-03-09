import strawberry
from datetime import datetime

@strawberry.type
class Account:
    id: str
    email: str
    date_of_birth: datetime
    account_number: str
    balance: float
    created_at: datetime