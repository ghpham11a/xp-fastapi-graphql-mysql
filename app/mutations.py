import uuid
import strawberry
from datetime import datetime
from typing import Optional

from app.models import Account

@strawberry.type
class Mutation:
    
    @strawberry.mutation
    async def create_account(
        self,
        info: strawberry.Info,
        email: str,
        date_of_birth: datetime,
        account_number: str,
        initial_balance: float = 0.0
    ) -> Account:
        request = info.context["request"]
        pool = request.app.state.pool

        new_id = str(uuid.uuid4())
        created_at = datetime.now(datetime.timezone.utc)

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = """
                INSERT INTO Accounts (Id, Email, DateOfBirth, AccountNumber, Balance, CreatedAt)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                await cur.execute(sql, (
                    new_id,
                    email,
                    date_of_birth,
                    account_number,
                    initial_balance,
                    created_at
                ))
                # If autocommit=False for your pool, call conn.commit() here.
        
        return Account(
            id=new_id,
            email=email,
            date_of_birth=date_of_birth,
            account_number=account_number,
            balance=initial_balance,
            created_at=created_at
        )

    @strawberry.mutation
    async def update_balance(self, info: strawberry.Info, id: str, new_balance: float) -> Optional[Account]:
        request = info.context["request"]
        pool = request.app.state.pool

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # 1) Fetch existing record
                await cur.execute("SELECT Id, Email, DateOfBirth, AccountNumber, Balance, CreatedAt FROM Accounts WHERE id=%s", (id,))
                row = await cur.fetchone()
                if not row:
                    return None  # No record found

                # 2) Update
                sql_update = "UPDATE Accounts SET balance=%s WHERE id=%s"
                await cur.execute(sql_update, (new_balance, id))

                # If autocommit=False for your pool, call conn.commit() here

                # 3) Rebuild the object for returning
                (id_, email, dob, account_num, old_balance, created_at) = row
                return Account(
                    id=id_,
                    email=email,
                    date_of_birth=dob,
                    account_number=account_num,
                    balance=new_balance,
                    created_at=created_at
                )