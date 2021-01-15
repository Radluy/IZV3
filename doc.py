import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_pickle("accidents.pkl.gz")
print(df)

df_m = pd.DataFrame()
df_m['vehicle_type'] = df.p44
df_m['village'] = df.p5a
print(df_m)

plt.figure(figsize=(20, 20))
ax = plt.gca()
df_m.plot(ax=ax)
plt.show()
#p44 == 13  //cyclist
#p5a == 1   //in village
#p5a == 2   //outside village