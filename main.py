from sodapy import Socrata

import argparse
import sys
import os
import requests
from requests.auth import HTTPBasicAuth

#DATASET_ID = "nc67-uf89"
#APP_TOKEN = "q04ia5gRnoMvCEigomLaSj3yc"
#INDEX_NAME = "violations5"
#ES_HOST = "https://search-sta9760f2021bena-iwyjfy4gdryoipo46uyctn3voa.us-east-2.es.amazonaws.com"
#ES_USERNAME = "bena"
#ES_PASSWORD = "Sta9760f2021bena@"

DATASET_ID = os.environ["DATASET_ID"]
APP_TOKEN = os.environ["APP_TOKEN"]
INDEX_NAME = os.environ["INDEX_NAME"]
ES_HOST = os.environ["ES_HOST"]
ES_USERNAME = os.environ["ES_USERNAME"]
ES_PASSWORD = os.environ["ES_PASSWORD"]

parser = argparse.ArgumentParser(description="Process data from payroll")
parser.add_argument("--page_size", type=int, help="How many rows to fetch per page", required=True)
parser.add_argument("--num_pages", type=int, help="How many pages to fetch")
args = parser.parse_args(sys.argv[1:])
print(args)


if __name__ == '__main__':
    resp = requests.get(ES_HOST, auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD))
    try:
        resp = requests.put(
            f"{ES_HOST}/{INDEX_NAME}",
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
            json={
                "settings": {
                    "number_of_shards":5,
                    "number_of_replicas":1,
                    
                },
                "mappings": {
                    "properties": {
                        "plate": {"type":"text"},
                        "state": {"type":"text"},
                        "license_type": {"type":"text"},
                        "summons_number": {"type":"text"},
                        "issue_date": {"type":"date","format": "MM/dd/yyyy"},
                        "violation_time": {"type":"text"},
                        "violation": {"type":"text"},
                        "judgement_entry_date": {"type":"text"},
                        "fine_amount": {"type":"integer"},
                        "penalty_amount": {"type":"integer"},
                        "interest_amount": {"type":"integer"},
                        "reduction_amount": {"type":"integer"},
                        "payment_amount": {"type":"integer"},
                        "amount_due": {"type":"integer"},
                        "precinct": {"type":"keyword"},
                        "county": {"type":"keyword"},
                        "issuing_agency": {"type":"keyword"},
                        "violation_status": {"type":"keyword"},

                    }
                }
            }
        )
        resp.raise_for_status()
    except Exception as e:
        print("Index already exists")
    
    client = Socrata(
        "data.cityofnewyork.us",
        APP_TOKEN,
    )
    for i in range(0,args.num_pages):
        rows = client.get(DATASET_ID, limit=args.page_size, order="summons_number")    
        for row in rows: 
            try:
                es_row = {}
                if "plate" in row:
                    es_row["plate"] = str(row["plate"])
                else:
                    es_row["plate"] = "MISSING"
                if "state" in row:
                    es_row["state"] = str(row["state"])
                else:
                    es_row["state"] = "MISSING"
                if "issue_date" in row:
                    es_row["issue_date"] = row["issue_date"]
                else:
                    es_row["issue_date"] = "MISSING"
                if "license_type" in row:
                    es_row["license_type"] = str(row["license_type"])
                else:
                    es_row["license_type"] = "MISSING"
                if "summons_number" in row:
                    es_row["summons_number"] = row["summons_number"]
                else:
                    es_row["summons_number"] = "MISSING"
                if "issue_date" in row:
                    es_row["issue_date"] = row["issue_date"]
                else:
                    es_row["issue_date"] = "MISSING"
                if "fine_amount" in row:
                    es_row["fine_amount"] = float(row["fine_amount"])
                else:
                    es_row["fine_amount"] = "MISSING"
                if "penalty_amount" in row:
                    es_row["penalty_amount"] = float(row["penalty_amount"])
                else:
                    es_row["penalty_amount"] = "MISSING"
                if "interest_amount" in row:
                    es_row["interest_amount"] = float(row["interest_amount"])
                else:
                    es_row["interest_amount"] = "MISSING"
                if "reduction_amount" in row:
                    es_row["reduction_amount"] = float(row["reduction_amount"])
                else:
                    es_row["reduction_amount"] = "MISSING"
                if "payment_amount" in row:
                    es_row["payment_amount"] = float(row["payment_amount"])
                else:
                    es_row["payment_amount"] = "MISSING"
                if "amount_due" in row:
                    es_row["amount_due"] = float(row["amount_due"])
                else:
                    es_row["amount_due"] = "MISSING"
                if "precinct" in row:
                    es_row["precinct"] = str(row["precinct"])
                else:
                    es_row["precinct"] = "MISSING"
                if "county" in row:
                    es_row["county"] = str(row["county"])
                else:
                    es_row["county"] = "MISSING"
                if "issuing_agency" in row:
                    es_row["issuing_agency"] = str(row["issuing_agency"])
                else:
                    es_row["issuing_agency"] = "MISSING"
                if "violation_status" in row:
                    es_row["violation_status"] = str(row["violation_status"])
                else:
                    es_row["violation_status"] = "MISSING"
            except Exception as e:
                print(f"Skipping because of failure:{e}")
            
            try:
                resp = requests.post(
                    f"{ES_HOST}/{INDEX_NAME}/_doc",
                    auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
                    json=es_row,
                )
                resp.raise_for_status()
            except Exception as e:
                    print("Failed to upload to elasticsearch")
            
            