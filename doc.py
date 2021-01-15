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

cycle = df_s[df_s['vehicle_type'] == 13]
cycle_vil = cycle[cycle['village'] == 1].count()
cycle_rur = cycle[cycle['village'] == 2].count()

moto = df_s[df_s['vehicle_type'] == 1]
moto_vil = moto[moto['village'] == 1].count()
moto_rur = moto[moto['village'] == 2].count()

print("počet cyklo nehôd v obci: {}".format(cycle_vil['village']))
print("počet cyklo nehôd mimo obce: {}".format(cycle_rur['village']))

print("počet motocyklo nehôd v obci: {}".format(moto_vil['village']))
print("počet motocyklo nehôd mimo obce: {}".format(moto_rur['village']))