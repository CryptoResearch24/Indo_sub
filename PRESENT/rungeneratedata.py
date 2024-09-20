from generatedata_nomal import generate_data
dataset_size= 200000
ptd= 0x90
for nrounds in range(2,21):
    filename= f"./Data/Round{nrounds}.csv"
    generate_data(dataset_size, ptd, nrounds, filename)
    print(f'Done round {nrounds}')
    