from fastapi import HTTPException


class Error:

    @classmethod
    def if_param_is_null_or_empty(cls, param,name):
        """
        Common success method for API response
        """
        if param == "" or param is None:
             raise HTTPException(status_code=400, detail=f"{name} is invalid or is empty")

    @classmethod
    def if_param_is_null_or_empty_or_not_valid(cls, param,name,is_valid):
        """
        Common success method for API response
        """
        if param == "" or param is None or not is_valid:
             raise HTTPException(status_code=400, detail=f"{name} is invalid or is empty")

