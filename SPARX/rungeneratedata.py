##################### run this file to generate dataset #####################

from SPARX_Data_Gen import generate_data

dataset_size= 100000

for n_rounds in range(3, 7):
    filename= f'./Data/Round{n_rounds}.csv'
    generate_data(dataset_size, n_rounds, filename)
    print(f'Done round {n_rounds}')
print("Done")
