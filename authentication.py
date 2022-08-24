"""Class for token authentication"""




from fastapi import HTTPException
from jwt_utility import JWTUtility
from sqlalchemy.orm import Session
from patient.app.models import models
from starlette.responses import Response


class Authentication():
    """Authenticate user using JWT utility """

    def authenticate(self, token,database: Session):
        """Authenticate function for authenticating apis """
        is_valid,_ = JWTUtility.is_token_valid(token)
        if is_valid:
            data = JWTUtility.decode_token(token)
            try:
                user = database.query(models.Patient).filter_by(
                    email=data["email"], contact_number=data["mobile_number"]).first()
                if not user:
                    raise HTTPException(status_code=400, detail="Invalid token")
            except Exception:
                raise HTTPException(status_code=400, detail="No such user exists or token is expired")
            return user, None
        else:
            raise HTTPException(status_code=400, detail="Please provide a valid token")
