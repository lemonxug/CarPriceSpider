import os

for f in os.listdir(os.getcwd())[:-2]:
    if '-' in f:
        nf = '_'.join(f.split('-'))
        os.rename(f, nf)
        print(nf)
