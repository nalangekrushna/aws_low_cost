import os, json, datetime, boto3

# response = ec2.describe_regions()
# regions = [ region['RegionName'] for region in response['Regions'] ]
# print(regions)
regions = ['ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
#regions = ['us-west-2']
services = ['ec2']
profile_name = 'billing'

today = datetime.datetime.now()
instance_prices = []
for region in regions :
    session = boto3.Session(profile_name=profile_name,region_name=region)
    for service in services :
        client = session.client(service)
        resp = client.describe_spot_price_history(
            InstanceTypes= [ 't3a.micro'],
            
            ProductDescriptions= ['Linux/UNIX'],
            StartTime=datetime.datetime.now(), # - datetime.timedelta(1),
            EndTime=datetime.datetime.now()
            )
        min_spot_price_region_instance = min(resp['SpotPriceHistory'], key=lambda x:x['SpotPrice'])
    instance_prices.append(min_spot_price_region_instance)
#print(instance_prices)
min_spot_price_all_regions = min(instance_prices, key=lambda x:x['SpotPrice'])
print(min_spot_price_all_regions)