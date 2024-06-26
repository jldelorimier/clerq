# ACME Payments Settlement API

## Overview

This API communicates with the ACME Payments system to fetch transaction details for a given merchant & settlement date, and return the net settlement amount for that merchange on that date.

### Settlement Endpoint

- **URL**: `/settlement/{merchant_id}`
- **Method**: GET
- **Description**: Retrieves settlement details for a specific merchant on a given settlement date.
- **Query Parameters**:
  - `merchant_id`: The unique identifier of the merchant.
  - `settlement_date`: The date for which settlement data is requested.
- **Response**:
  - `merchant_id`: The ID of the merchant.
  - `settlement_date`: The requested settlement date.
  - `settlement_amount`: The total settlement amount for the merchant on the specified date.
- **Error Handling**: 
  - Returns an HTTP 400 error if there is an issue fetching data from the ACME Payments API.
  - Implements retry logic for retryable exceptions such as HTTPError and RequestException.

## Usage

To use this API, make HTTP GET requests to the appropriate endpoints with the required parameters. Ensure that you provide valid `merchant_id` and `settlement_date` values.

Example:
- GET http://127.0.0.1:8000/settlement/98f9d65c-6dd8-46a9-8850-f5afd9a49013?settlement_date=2022-12-11 HTTP/1.1
- Host: 127.0.0.1:8000

## To get this project running:
### 1. Clone the repository:
Clone this repo to your local machine: `git clone https://github.com/jldelorimier/clerq.git` 
### 2. Create a virtual environment:
Navigate to the project directory `cd clerq`, and create a virtual environment: `python3 -m venv venv`
### 3. Activate the virtual environment:
  - macOS/Linux: `source venv/bin/activate`
  - Windows: `venv/Scripts/activate`
### 4. Install project dependencies: 
Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt` depending on your local version.
### 5. Start the application:
Run the FastAPI server: `uvicorn main:app --reload`
### 6. See the application running:
Navigate to `http://127.0.0.1:8000/` in a browser
### 7. Append the url with necessary data to get the settlement data for a given merchant and date:
`http://127.0.0.1:8000/settlement/:merchant_id?settlement_date=YYYY-MM-DD`
Replace `:merchant_id` with the merchant's ID and `YYYY-MM-DD` with the desired settlement date in the format YYYY-MM-DD.
