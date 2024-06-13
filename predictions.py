from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  
import pandas as pd

class InsuranceData(BaseModel):
  policyno: str = None
  age: int
  gender: str
  annualincome: float
  occupation: str
  education: str
  sumassured: float
  annualpremium: float
  premfreq: int
  affscore: int

app = FastAPI()

@app.post("/predict_risk")
async def predict_risk(data: InsuranceData):
  """
  This function receives policy data and returns the risk profile of the policy.
  """

  # Replace with your actual data source (e.g., database connection)

  policy_data = {'Policy No': ['P2378AH', 'P6689GD', 'P0089TU','P5567BU','P9545VZ'], 'Risk Probability': [0.92, 0.54, 0.12,0.62,0.84], 'Risk Bucket': ['Bucket 1', 'Bucket 29', 'Bucket 46','Bucket 33','Bucket 2'], 'Risk Category': ['High Risk', 'Moderate Risk', 'Low Risk', 'Moderate Risk','High Risk']}
    
      
  df = pd.DataFrame(policy_data)
    
    # Check for missing required fields (modify based on your needs)
  if data.age < 0:
     raise HTTPException(status_code=406, detail="Age must be a positive number.")
      
    # Filter data by policy number
  filtered_df = df[df["Policy No"] == data.policyno]
      
    # Return the DataFrame as a dictionary (for JSON serialization)
  return filtered_df.to_dict(orient="records")


