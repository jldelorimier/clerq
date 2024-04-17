from fastapi import FastAPI, HTTPException
from datetime import date, timedelta
import requests

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "This is the ACME Payments Settlement API"}

@app.get("/settlement/{merchant_id}")
async def get_settlement(merchant_id: str, settlement_date: date):
  try:
    api_url = "https://api-engine-dev.clerq.io/tech_assessment/transactions/"
    
    response = requests.get(api_url, params={
      "merchant": merchant_id,
      "created_at_gte": settlement_date,
      "created_at_lt": settlement_date + timedelta(days=1)
    })
    response.raise_for_status()
    data = response.json()
    
    print(data)
    transactions = data["results"]

    payments = sum(txn['amount'] for txn in transactions if txn['type'] == 'PURCHASE')
    refunds = sum(txn['amount'] for txn in transactions if txn['type'] == 'REFUND')

    settlement_amount = payments - refunds

    return {
      "merchat_id": merchant_id, 
      "settlement_date": settlement_date.isoformat(), 
      "settlement_amount": settlement_amount 
    }
  except requests.exceptions.RequestException as error:
    raise HTTPException(status_code=400, detail=f"Error fetching data from ACME Payments API: {str(error)}")
                       