from hashlib import sha256

from fastapi import Depends, APIRouter, HTTPException

from app.config.settings import project_settings
from app.models import User
from app.repositories.payment_repository import PaymentRepository
from app.schemas.account import AccountResponse
from app.repositories.account_repository import AccountRepository
from app.schemas.payment import PaymentRequest
from app.services.access_service import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{account_id}")
async def get_account(
        account_id: int,
        accountRepository: AccountRepository=Depends(),
        current_user: User = Depends(get_current_user),
) -> AccountResponse:
    account = await accountRepository.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if not current_user.is_admin and account not in current_user.accounts:
        raise HTTPException(status_code=403)
    return AccountResponse.model_validate(account)

@router.post("/hook")
async def create_payment(
        payment: PaymentRequest,
        accountRepository: AccountRepository=Depends(),
        paymentRepository: PaymentRepository=Depends()
) -> bool:
    sign = f"{payment.account_id}{payment.amount}{payment.transaction_id}{payment.user_id}{project_settings.PAYMENT_SECRET}"
    if sha256(sign.encode()) != payment.signature:
        raise HTTPException(status_code=403)
    account = await accountRepository.get(payment.account_id)
    if not account:
        await accountRepository.create(payment.account_id, payment.user_id, payment.amount)
    await paymentRepository.create(payment.account_id, payment.amount)
    return True