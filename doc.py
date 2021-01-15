import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#1 2 9 13 15
#p44 == 13  //cyclist
#p5a == 1   //in village
#p5a == 2   //outside village
df = pd.read_pickle("accidents.pkl.gz")

df_m = pd.DataFrame()
df_m['vehicle_type'] = df.p44
df_m['village'] = df.p5a
vals = [13, 15, 9, 1, 2]
df_s = df_m[df_m["vehicle_type"].isin(vals)]

ax = sns.countplot(data=df_s, x="vehicle_type", hue="village")
ax.set(yscale="log")
ax.legend(labels=["V obci", "Mimo obce"])
ax.set_xticklabels(["Malý motocykel", "motocykel", "traktor", 
                    "bicykel", "iné nemotorové\nvozidlo"])
plt.xlabel("")
plt.ylabel("Počet")
#plt.xticks(rotation=-15)
#plt.show()

plt.savefig("fig.png")

