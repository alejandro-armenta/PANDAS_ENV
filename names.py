import pandas as pd
import matplotlib.pyplot as plt

names = pd.read_csv("names.csv", index_col=0)

#print(names)

total_births = names.pivot_table(
    values="births",
    index="year",
    aggfunc="sum",
    columns="sex"
    )


#print(total_births.tail())

total_births.plot(
    title="Total births by sex and year", 
    ylabel="births in millions"
    )

plt.tight_layout()
plt.savefig("births.png")

def add_prop(group):
    #estos son los sexos por año 
    group["prop"] = group["births"] / group["births"].sum()
    return group

names = names.groupby(["year","sex"]).apply(add_prop)

print(names.query("year == 1880 & sex == 'F'"))







