import os
months = os.listdir('./pathDataCleansed')

for month in months:
    files = os.listdir('./pathDataCleansed/{}'.format(month))
    for file in files:
        os.remove('./pathDataCleansed/{}/{}'.format(month, file))