from fastapi import FastAPI, HTTPException
from datetime import date, timedelta
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from requests.exceptions import HTTPError, RequestException

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "This is the ACME Payments Settlement API"}

def is_retryable_exception(exception):
  """Return True if the exception is a type that should trigger a retry."""
  return isinstance(exception, (HTTPError, RequestException))

@retry(stop=stop_after_attempt(10), wait=wait_fixed(2), retry=retry_if_exception_type(is_retryable_exception))
async def make_api_request(merchant_id: str, settlement_date: date):
  api_url = "https://api-engine-dev.clerq.io/tech_assessment/transactions/"    
  response = requests.get(api_url, params={
    "merchant": merchant_id,
    "created_at_gte": settlement_date,
    "created_at_lt": settlement_date + timedelta(days=1)
  })
  response.raise_for_status()
  return response.json()


@app.get("/settlement/{merchant_id}")
async def get_settlement(merchant_id: str, settlement_date: date):
  try:    
    data = await make_api_request(merchant_id, settlement_date)
    transactions = data["results"]

    payments = sum(float(txn['amount']) for txn in transactions if txn['type'] == 'PURCHASE')
    refunds = sum(float(txn['amount']) for txn in transactions if txn['type'] == 'REFUND')

    settlement_amount = payments - refunds

    return {
      "merchant_id": merchant_id, 
      "settlement_date": settlement_date.isoformat(), 
      "settlement_amount": settlement_amount 
    }
  except HTTPError as error:
    raise HTTPException(status_code=400, detail=f"Error fetching data from ACME Payments API: {str(error)}")
                       