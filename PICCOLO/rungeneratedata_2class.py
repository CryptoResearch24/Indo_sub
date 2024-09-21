##################### run this file to generate dataset #####################
from generatedata_2class import generate_data


dataset_size= 100000
ptd2=  [0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x08]
for nrounds in range(2,5):
    filename= f"Piccolo80/Data/2Class_Round{nrounds}.csv"
    generate_data(dataset_size, ptd2, nrounds, filename)
    print(f'Done round {nrounds}')