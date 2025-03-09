import uuid
from datetime import datetime
from typing import List, Optional

import strawberry

import app.ACCOUNTS_DB

@strawberry.type
class Query:

    @strawberry.field
    def get_accounts(self) -> List[Account]:
        """Return all accounts."""
        return ACCOUNTS_DB

    @strawberry.field
    def get_account_by_id(self, id: str) -> Optional[Account]:
        """
        Return a single account by its ID or None if not found.
        """
        for account in ACCOUNTS_DB:
            if account.id == id:
                return account
        return None