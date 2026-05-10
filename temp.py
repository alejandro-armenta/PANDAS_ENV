import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


fec = pd.read_csv("datasets/fec/P00000001-ALL.csv", low_memory=False)

#print(fec)

#fec.info()


parties = {
    "Bachmann, Michelle": "Republican",
"Cain, Herman": "Republican",
"Gingrich, Newt": "Republican",
"Huntsman, Jon": "Republican",
"Johnson, Gary Earl": "Republican",
"McCotter, Thaddeus G": "Republican",
"Obama, Barack": "Democrat",
"Paul, Ron": "Republican",
"Pawlenty, Timothy": "Republican",
"Perry, Rick": "Republican",
"Roemer, Charles E. 'Buddy' III": "Republican",
"Romney, Mitt": "Republican",
"Santorum, Rick": "Republican"
}

#print(parties)


fec['party'] = fec['cand_nm'].map(parties)

"""
print(fec['party'].value_counts())

print(
    (fec['contb_receipt_amt'] > 0).value_counts()
)
"""

fec = fec[(fec['contb_receipt_amt'] > 0)]

bomr = (
    fec[
        fec["cand_nm"].
        isin(
            ["Obama, Barack","Romney, Mitt"]
        )
    ]
)


occ_mapping = {
"INFORMATION REQUESTED PER BEST EFFORTS" : "NOT PROVIDED",
"INFORMATION REQUESTED" : "NOT PROVIDED",
"INFORMATION REQUESTED (BEST EFFORTS)" : "NOT PROVIDED",
"C.E.O.": "CEO"
}

def get_occ(x):
    return occ_mapping.get(x, x)

fec["contbr_occupation"] = fec["contbr_occupation"].map(get_occ)


emp_mapping = {
"INFORMATION REQUESTED PER BEST EFFORTS" : "NOT PROVIDED",
"INFORMATION REQUESTED" : "NOT PROVIDED",
"SELF" : "SELF-EMPLOYED",
"SELF EMPLOYED" : "SELF-EMPLOYED",
}

def get_emp(x):
    return emp_mapping.get(x, x)

fec["contbr_employer"] = fec["contbr_employer"].map(get_emp)

#fec.info()
#############################################################

by_occ = (
    fec.
    pivot_table(
        "contb_receipt_amt", 
        index="contbr_occupation",
        columns="party",
        aggfunc="sum"
    )
)

over_2 = (
    by_occ[
        by_occ.
        sum(axis="columns") > 2000000
    ]
)

over_2.plot(kind="barh")
plt.tight_layout()
plt.savefig("occ.png")

def get_top_amounts(group, key, n=5):
    """
    la ocupacion del donador de barack obama
    la ocupacion del donador de rommey
    """

    return (
        group.
        groupby(key)['contb_receipt_amt'].
        sum().
        nlargest(n)
    )

"""
print(
    bomr.
    groupby("cand_nm").
    apply(
        get_top_amounts, 
        'contbr_occupation', 
        7
    )
)

print(
    bomr.
    groupby("cand_nm").
    apply(
        get_top_amounts, 
        'contbr_employer', 
        10
    )
)
"""

bins= np.array(
    [0,1,10,100,1000,10000,100_000,1_000_000,10_000_000]
               )
labels = (
    pd.cut(
        bomr['contb_receipt_amt'], 
        bins=bins
    )
)

#print(labels.sort_index())
#print(bomr)

#bomr.info()

bucket_sums = (
    bomr.
    groupby(
        ["cand_nm",labels]
    )
    ['contb_receipt_amt'].
    sum().
    unstack(level=0)
)

#print(bucket_sums)
#print(bucket_sums.sum(axis="columns"))

normed_sums = (
    bucket_sums.
    div(
        bucket_sums.sum(axis="columns"),
        axis="index"
    )
)

plt.close('all')
normed_sums.plot(kind="barh")
plt.tight_layout()
plt.savefig("proportions.png")



"""

print(
    bomr.
    groupby(
        ["cand_nm",labels]
    ).
    size().
    unstack(level=0)
)



bomr.info()
"""

totals = (

    bomr.
    
    groupby(
        [
            "cand_nm",
            "contbr_st"
        ]
    )
    ["contb_receipt_amt"].

    sum().
    
    unstack(level=0).
    
    fillna(0)

)

totals = (
    totals[totals.sum(axis="columns") > 100_000]
    )

print(totals.div(totals.sum(axis="columns"), axis="index").sum(axis='columns'))


print(totals.div(totals.sum(axis="columns"), axis="index"))
