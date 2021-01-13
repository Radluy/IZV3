#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
import cartopy.crs as ccrs
# muzeze pridat vlastni knihovny



def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""
    df = df.loc[df['region'] == 'JHM']
    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df["d"], df["e"]), crs="EPSG:5514"
    )
    gdf = gdf.to_crs("EPSG:3857")
    return gdf


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s dvemi podgrafy podle lokality nehody """
    fig,ax=plt.subplots(1,2,figsize=(12,11))
    gdf[gdf["p5a"]==1].plot(ax=ax[0], markersize=1).set_title("Nehody v JHM kraji: V obci")
    ctx.add_basemap(ax[0],crs=gdf.crs.to_string(),
                    source=ctx.providers.Stamen.TonerLite,zoom=10, alpha=0.9)

    gdf[gdf["p5a"]==2].plot(ax=ax[1], markersize=1, color="r").set_title("Nehody v JHM kraji: Mimo obce")
    ctx.add_basemap(ax[1],crs=gdf.crs.to_string(),
                    source=ctx.providers.Stamen.TonerLite,alpha=0.9, zoom=10)

    ax[0].axis("off")
    ax[1].axis("off")

    if (fig_location):
        plt.savefig(fig_location)

    if (show_figure):
        plt.show()


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """



if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)

