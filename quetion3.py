import boto3

def get_billed_regions():
    ce = boto3.client('ce')

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={'Start': '2025-01-01', 'End': '2025-02-15'},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'REGION'}]
        )

        return list({group['Keys'][0] for time_period in response['ResultsByTime'] 
                     for group in time_period.get('Groups', []) 
                     if float(group['Metrics']['UnblendedCost']['Amount']) > 0})

    except Exception:
        return []

if __name__ == "__main__":
    regions = get_billed_regions()
    print("Billed regions are: ")
    print(regions if regions else "No billed regions found.")
