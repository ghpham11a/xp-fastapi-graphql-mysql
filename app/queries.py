import uuid
from datetime import datetime
from typing import List, Optional

import strawberry

from app.models import Account

@strawberry.type
class Query:

    @strawberry.field
    async def get_accounts(self, info: strawberry.Info) -> List[Account]:
        """
        Example query to fetch all rows from an `accounts` table.
        """
        request = info.context["request"]
        pool = request.app.state.pool

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT Id, Email, DateOfBirth, AccountNumber, Balance, CreatedAt FROM Accounts")
                rows = await cur.fetchall()
                # rows is a list of tuples by default
                # If you want dictionaries, use: cursor(aiomysql.DictCursor)

        # Convert rows to List[Account]
        accounts = []
        for (id_, email, dob, account_num, balance, created_at) in rows:
            accounts.append(Account(
                id=id_,
                email=email,
                date_of_birth=dob,
                account_number=account_num,
                balance=balance,
                created_at=created_at
            ))
        return accounts