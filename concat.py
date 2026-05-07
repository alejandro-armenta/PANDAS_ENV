import pandas as pd

names1880 = pd.read_csv('datasets/babynames/yob1880.txt',names=["name", "sex","births"])

#en 1880
#print(names1880.groupby("sex")['births'].sum())

pieces = []
for year in range(1880,2011):
    path =  f"datasets/babynames/yob{year}.txt"
    #print(path)
    frame = pd.read_csv(path, names=["name", "sex","births"])
    frame["year"] = year

    #print(frame)

    pieces.append(frame)

print(len(pieces))

df = pd.concat(pieces, ignore_index=True)
df.to_csv("names.csv")
