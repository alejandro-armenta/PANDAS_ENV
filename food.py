import pandas as pd
import matplotlib.pyplot as plt

ndata = pd.read_pickle("ndata.pkl")

result = (
    ndata.
    groupby(
        ["nutrient","fgroup"]
    )["value"].
    quantile(0.5)
)

result["Zinc, Zn"].sort_values().plot(kind="barh")
plt.tight_layout()
plt.savefig("zinc.png")

def get_maximum(group):
    return group.loc[group.value.idxmax()]

max_foods = (
    ndata.
    groupby(
        ["nutgroup","nutrient"]
    ).
    apply(get_maximum)
    [["value","food"]]
)


