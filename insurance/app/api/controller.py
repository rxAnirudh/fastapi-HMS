import sys

from fastapi import HTTPException
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from insurance.app.models import models,schemas
from response import Response as ResponseData
from patient.app.api.controller import check_if_patient_id_is_valid


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_insurance(database: Session, insurance: schemas.InsuranceBase):
    """Function to add new insurance details for particular patient"""
    if not check_if_patient_id_is_valid(database,insurance.dict()["patient_id"]):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    insurance_dict = {'patient_id': insurance.dict()["patient_id"], 'policy_no': insurance.dict()["policy_no"],"expire_date" : insurance.dict()["expire_date"],
    "maternity" : insurance.dict()["maternity"],"dental" : insurance.dict()["dental"],"optical" : insurance.dict()["optical"],"chronic_pec" : insurance.dict()["chronic_pec"]}
    db_insurance = models.Insurance(**insurance_dict)
    database.add(db_insurance)
    database.commit()
    database.refresh(db_insurance)
    insurance_cover_dict = {'ins_company': insurance.dict()["ins_company"],"ins_plan" : insurance.dict()["ins_plan"],
    "co_pay" : insurance.dict()["co_pay"],"co_insurance" : insurance.dict()["co_insurance"],"med_coverage" : insurance.dict()["med_coverage"],
    "entry_fees" : insurance.dict()["entry_fees"],"id" : db_insurance.id,}
    db_insurance_cover_details = models.InsuranceCover(**insurance_cover_dict)
    database.add(db_insurance_cover_details)
    database.commit()
    database.refresh(db_insurance_cover_details)
    Merge(insurance_dict, insurance_cover_dict)
    return ResponseData.success(insurance_cover_dict,"Insurance added successfully")

def get_insurance_details_by_id(database: Session, id : Optional[int] = None):
    """Function to get insurance details of patient based on id"""
    if id is None:
        db_insurance = database.query(models.Insurance).filter().first()
        db_insurance_cover_details = database.query(models.InsuranceCover).filter().first()
        Merge(db_insurance.__dict__, db_insurance_cover_details.__dict__)
        return ResponseData.success(db_insurance_cover_details.__dict__,"Insurance details fetched successfully")
    db_insurance = database.query(models.Insurance).filter(models.Insurance.id == id).first()
    if db_insurance is None:
        return ResponseData.success([],"Insurance with this id does not exists")
    db_insurance_cover_details = database.query(models.InsuranceCover).filter(models.InsuranceCover.id == id).first()
    Merge(db_insurance.__dict__, db_insurance_cover_details.__dict__)
    return ResponseData.success(db_insurance_cover_details.__dict__,"Insurance details fetched successfully")

def delete_insurance_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all insurance details if needed"""
    if id is None:
        database.query(models.Insurance).delete()
        database.commit()
        return ResponseData.success([],"All insurance details deleted successfully")
    database.query(models.Insurance).filter_by(id = id).delete()
    database.query(models.InsuranceCover).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Insurance details deleted successfully")

def update_insurance_details(database: Session, insurance: schemas.AddNewInsurance):
    """Function to update insurance details of a particular patient"""
    data = database.query(models.InsuranceCover,models.Insurance).filter(models.Insurance.id == insurance.id).all()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Id is invalid")
    dict1 = data[0]["InsuranceCover"]
    dict2 = data[0]["Insurance"]
    if insurance.dict()["policy_no"] is not None :
        dict2.__dict__["policy_no"] = insurance.dict()["policy_no"]
    if insurance.dict()["publish_date"] is not None :
        dict2.__dict__["publish_date"] = insurance.dict()["publish_date"]
    if insurance.dict()["expire_date"] is not None :
        dict2.__dict__["expire_date"] = insurance.dict()["expire_date"]
    if insurance.dict()["maternity"] is not None :
        dict2.__dict__["maternity"] = insurance.dict()["maternity"]
    if insurance.dict()["dental"] is not None :
        dict2.__dict__["dental"] = insurance.dict()["dental"]
    if insurance.dict()["optical"] is not None :
        dict2.__dict__["optical"] = insurance.dict()["optical"]
    if insurance.dict()["chronic_pec"] is not None :
        dict2.__dict__["chronic_pec"] = insurance.dict()["chronic_pec"]
    if insurance.dict()["ins_company"] is not None :
        dict1.__dict__["ins_company"] = insurance.dict()["ins_company"]
    if insurance.dict()["ins_plan"] is not None :
        dict1.__dict__["ins_plan"] = insurance.dict()["ins_plan"]
    if insurance.dict()["entry_fees"] is not None :
        dict1.__dict__["entry_fees"] = insurance.dict()["entry_fees"]
    if insurance.dict()["co_pay"] is not None :
        dict1.__dict__["co_pay"] = insurance.dict()["co_pay"]
    if insurance.dict()["co_insurance"] is not None :
        dict1.__dict__["co_insurance"] = insurance.dict()["co_insurance"]
    if insurance.dict()["med_coverage"] is not None :
        dict1.__dict__["med_coverage"] = insurance.dict()["med_coverage"]
    
    database.query(models.Insurance).filter(models.Insurance.id == insurance.id).update({ models.Insurance.id : insurance.id,
        models.Insurance.policy_no: dict2.__dict__["policy_no"],
        models.Insurance.expire_date : dict2.__dict__["expire_date"],
        models.Insurance.maternity : dict2.__dict__["maternity"],
        models.Insurance.dental : dict2.__dict__["dental"],
        models.Insurance.optical : dict2.__dict__["optical"],
        models.Insurance.chronic_pec : dict2.__dict__["chronic_pec"],
        models.Insurance.publish_date : dict2.__dict__["publish_date"],
        
    })
    database.query(models.InsuranceCover).filter(models.InsuranceCover.id == insurance.id).update({
        models.InsuranceCover.id : insurance.id,
        models.InsuranceCover.ins_company : dict1.__dict__["ins_company"],
        models.InsuranceCover.ins_plan : dict1.__dict__["ins_plan"],
        models.InsuranceCover.entry_fees : dict1.__dict__["entry_fees"],
        models.InsuranceCover.co_pay : dict1.__dict__["co_pay"],
        models.InsuranceCover.co_insurance : dict1.__dict__["co_insurance"],
        models.InsuranceCover.med_coverage : dict1.__dict__["med_coverage"],
    })
    database.flush()
    database.commit()
    dict1.__dict__.update(dict2.__dict__)
    return ResponseData.success(dict1.__dict__,"Insurance details for this patient updated successfully")
