"""Class for token authentication"""




from fastapi import HTTPException
from jwt_utility import JWTUtility
from sqlalchemy.orm import Session
from patient.app.models import models
from appointment.app.models import models as appointmentmodels
from starlette.responses import Response


class Authentication():
    """Authenticate user using JWT utility """

    def authenticate(self, token,database: Session):
        """Authenticate function for authenticating apis """
        is_valid,_ = JWTUtility.is_token_valid(token)
        if is_valid:
            data = JWTUtility.decode_token(token)
            try:
                print(f"user before {data}")
                # user = database.query(appointmentmodels.Appointment).filter(models.Patient.email == data["email"],models.Patient.contact_number == data["mobile_number"]).first()
                user = database.query(models.Patient).filter_by(
                    email=data["email"] , contact_number = data["mobile_number"]).first()
                print(f"user after {user}")
                if not user:
                    raise HTTPException(status_code=400, detail="Invalid token")
            except Exception:
                raise HTTPException(status_code=400, detail="No such user exists or token is expired")
            return user, None
        else:
            raise HTTPException(status_code=400, detail="Please provide a valid token")
