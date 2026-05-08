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

names = (
    names.
    groupby(["year","sex"]).
    apply(add_prop).
    reset_index(drop=True)
)

sum_alex = names.groupby(["year","sex"])['prop'].sum()

#print(len(sum_alex[sum_alex == 1]) == len(sum_alex))

def get_top100(group):
    return group.sort_values("births",ascending=False)[:1000]
    

top1000 = names.groupby(["year","sex"]).apply(get_top100)

top1000 = top1000.reset_index(drop=True)

###################################################################

boys = top1000[top1000["sex"] == 'M']
girls = top1000[top1000["sex"] == 'F']


total_births = top1000.pivot_table("births", index="year", aggfunc="sum", columns="name")


subset = total_births[["John","Harry","Mary","Marilyn"]]

subset.plot(subplots=True, figsize=(12,10), title="Number of births per year")
plt.tight_layout()
plt.savefig("subset.png")

table = top1000.pivot_table("prop", index="year",aggfunc="sum", columns="sex")

table.plot(title="sum of table.prop")
plt.tight_layout()
plt.savefig("increase_variance.png")



df = boys[boys["year"] == 2010]

prop_cumsum = df["prop"].sort_values(ascending=False).cumsum()

#esta buscando la media desde los mas comunes hasta los menos comunes
#116 / 1000
#print(prop_cumsum.searchsorted(0.5))


df = boys[boys["year"] == 1900]

prop_cumsum = df["prop"].sort_values(ascending=False).cumsum()

#esta buscando la media desde los mas comunes hasta los menos comunes
#116 / 1000

#para llegar a la media hay mas diversidad ahora que en 1900

#print(prop_cumsum.searchsorted(0.5))

def get_quantile_count(group, q = 0.5):

    return ( 
        group.
        
        sort_values(
            "prop",
            ascending=False
        ).
        
        prop.
        
        cumsum().
        
        searchsorted(q) + 1
    )


diversity = (

    top1000.

    groupby(["year","sex"]).

    apply(get_quantile_count).

    unstack()

)

diversity.plot(title="cumulative plot name frequency to median")
plt.tight_layout()
plt.savefig("cumulative.png")


def get_last_letter(x):
    return x[-1]

#estos si son todos
last_letters = (
    names["name"].
    map(get_last_letter)
)

#print(last_letters)

last_letters.name = "last_letter"

#print(last_letters)

#sumo todos los births que terminan con la a por año
table = (
    names.
    pivot_table(
        "births", 
        index=last_letters, 
        columns=["sex","year"], 
        aggfunc="sum"
    )
)

subtable = (
    table.
    reindex(level="year", columns=[1910,1960,2010])
)

#print((subtable / subtable.sum()).sum())

letter_prop = (subtable / subtable.sum())



fig,axes = (
    plt.
    subplots(
        2,
        1,
        figsize=(10,8)
    )
)

(
    letter_prop["M"].
    plot(
        kind="bar", 
        title="male", 
        rot=0, 
        ax=axes[0]
    )
)


(
    letter_prop["F"].
    plot(
        kind="bar", 
        title="female", 
        rot=0, 
        ax=axes[1]
    )
)

plt.tight_layout()
plt.savefig("proportions.png")


#print((table / table.sum()).sum())

letter_prop = (table / table.sum())

male = (
    letter_prop.
    loc[
        ["d","n","y"], 
        "M"
    ].
    T
)


male.plot()
plt.savefig("male.png")



all_names = (
    pd.Series(
        top1000["name"].
        unique()
    )
)

lesley_like = (
    all_names[
        all_names.
        str.
        contains("Lesl")
    ]
)


filtered = (
    top1000[
        top1000["name"].
        isin(lesley_like)
    ]
)

#print(filtered.groupby("name")["births"].sum())

table = (
    filtered.
    pivot_table(
        "births", 
        index="year", 
        aggfunc="sum", 
        columns="sex"
    )
)

#es el total por año
"""
print(
    table.
    div(
        table.
        sum(axis="columns"), 
        axis="index"
    ).sum(axis="columns")
)
"""

table = (
    table.
    div(
        table.
        sum(axis="columns"), 
        axis="index"
    )
)


plt.close('all')

(
    table.
    plot(
        title="leslies as men or women in time.",
        ylabel="proportion",
        style=
        {
            "M":"r-",
            "F":"b--"
        }
    )
)

plt.tight_layout()
plt.savefig("leslies.png")





