from decimal import Decimal
from uuid import UUID

class UserNotFoundError(Exception):
    def __init__(
            self,
            user_id: UUID,
    ) -> None:
        self.user_id = user_id
        super().__init__(f"User '{user_id}' was not found.")

class InsufficientBalanceError(Exception):
    def __init__(
            self,
            user_id: UUID,
            balance: Decimal,
            amount: Decimal,
    ) -> None:
        self.user_id = user_id
        self.balance = balance
        self.amount = amount
        super().__init__(f"User '{user_id}' has insufficient balance.")