import uuid
from datetime import datetime
from typing import List, Optional

import strawberry

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_account(
        self,
        email: str,
        date_of_birth: datetime,
        account_number: str,
        initial_balance: float = 0.0
    ) -> Account:
        """
        Create a new account.
        
        - Automatically generates a UUID for the `id`.
        - Sets `created_at` to the current time.
        """
        new_account = Account(
            id=str(uuid.uuid4()),
            email=email,
            date_of_birth=date_of_birth,
            account_number=account_number,
            balance=initial_balance,
            created_at=datetime.utcnow()
        )
        ACCOUNTS_DB.append(new_account)
        return new_account

    @strawberry.mutation
    def update_balance(self, id: str, new_balance: float) -> Optional[Account]:
        """
        Update the balance of the account with the given ID.
        Returns the updated account or None if not found.
        """
        for account in ACCOUNTS_DB:
            if account.id == id:
                # Replace the old Account object with an updated version
                updated_account = Account(
                    id=account.id,
                    email=account.email,
                    date_of_birth=account.date_of_birth,
                    account_number=account.account_number,
                    balance=new_balance,
                    created_at=account.created_at
                )
                index = ACCOUNTS_DB.index(account)
                ACCOUNTS_DB[index] = updated_account
                return updated_account
        return None