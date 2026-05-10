import pandas as pd
import json

db = (
    json.
    load(
        open(
            "datasets/usda_food/database.json"
        )
    )
)


#print(db[0]["nutrients"][0])

nutrients = pd.DataFrame(db[0]["nutrients"])

info_keys = ["description","group","id","manufacturer"]

info= pd.DataFrame(db, columns=info_keys)

#info.info()

#print(info.value_counts(info["group"]))

nutrients = []

for rec in db:
    
    df = pd.DataFrame(rec["nutrients"])
    
    df["id"] = rec["id"]

    #print(df)

    nutrients.append(df)

nutrients = (
    pd.concat(nutrients, ignore_index=True)
)

#print(nutrients.duplicated().sum())

nutrients = nutrients.drop_duplicates()

#print(info)
#print(nutrients)

col_mapping = {
    "description":"food",
    "group":"fgroup"
}

info = (
    info.
    rename(
        columns=col_mapping, 
        copy=False
    )
)


col_mapping = {
    "description":"nutrient",
    "group":"nutgroup"
}

nutrients = (
    nutrients.
    rename(
        columns=col_mapping, 
        copy=False
    )
)

#denormalizacion
ndata = (pd.merge(nutrients,info, on="id"))

ndata.to_pickle("ndata.pkl")

result = (
    ndata.
    groupby(
        ["nutrient","fgroup"]
    )["value"].
    quantile(0.5)
)







    


