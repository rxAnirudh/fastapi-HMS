from fastapi import HTTPException
from doctor.app.response import Response as ResponseData


class Error:

    @classmethod
    def if_param_is_null_or_empty(cls, param,name):
        """
        Common success method for API response
        """
        if param == "" or param is None:
             return True
        else:
             return False

    @classmethod
    def if_param_is_null_or_empty_or_not_valid(cls, param,name,is_valid):
        """
        Common success method for API response
        """
        if param == "" or param is None or not is_valid:
             raise HTTPException(status_code=400, detail=f"{name} is invalid or is empty")

