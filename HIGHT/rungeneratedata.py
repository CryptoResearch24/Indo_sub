
from gendata_2class import generate_data

dataset_size= 500000

# n_rounds=2
for n_rounds in range(2, 3):
    filename= f'./Data/2class_HIGHT_round{n_rounds}_new.csv'
    generate_data(dataset_size, n_rounds, filename)
    print(f'Done round {n_rounds}')
print("Done")
