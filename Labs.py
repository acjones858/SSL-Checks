import requests
import json
import time

# Read domains from ssl.txt file
with open('ssl.txt', 'r') as file:
    domains = [line.strip() for line in file]

# Iterate over each domain
for domain in domains:
    print(f"Checking SSL grade for {domain}...")

    # Submit the domain to SSL Labs and get the analysis ID
    response = requests.post('https://api.ssllabs.com/api/v3/analyze', data={'host': domain})
    analysis_id = response.json()['analysisId']

    # Check the status of the analysis using the analysis ID
    while True:
        response = requests.get(f"https://api.ssllabs.com/api/v3/analyze/{analysis_id}")
        analysis_status = response.json()['status']

        if analysis_status == 'READY':
            break
        elif analysis_status == 'ERROR':
            print(f"An error occurred while analyzing {domain}.")
            break

        # Wait for 10 seconds before checking again
        time.sleep(10)

    if analysis_status == 'READY':
        # Get the SSL grade for the domain
        grade = response.json()['endpoints'][0]['grade']
        print(f"The SSL grade for {domain} is {grade}")

    print()
