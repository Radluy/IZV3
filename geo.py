#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np

def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    '''
    Plots the types of surfaces when car crashes happened.

            Parameters:
                    df (pd.DataFrame): DataFrame with data to plot
                    fig_location (str): File name to save figure
                    show_figure (bool): Whether to show figure

    '''
    df = df.loc[df['region'] == 'JHM']
    df.dropna(axis='rows', inplace=True)
    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df["d"], df["e"]), crs="EPSG:5514"
    )
    gdf = gdf.to_crs("EPSG:3857")
    return gdf


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    '''
    Plots the accidents to map, split by whether they
    happened in a village or not.

            Parameters:
                    gdf (geopandas.GeoDataFrame): GeoDataFrame with data to plot
                    fig_location (str): File name to save figure
                    show_figure (bool): Whether to show figure

    '''
    fig,ax=plt.subplots(1,2,figsize=(20,18))
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
    '''
    Plots the accidents aggregated into 12 clusters onto a map.

            Parameters:
                    gdf (geopandas.GeoDataFrame): GeoDataFrame with data to plot
                    fig_location (str): File name to save figure
                    show_figure (bool): Whether to show figure

    '''
    coords = np.dstack([gdf.geometry.x, gdf.geometry.y]).reshape(-1, 2)
    db = sklearn.cluster.MiniBatchKMeans(n_clusters=12).fit(coords)

    gdf1 = gdf.copy()
    gdf1["cluster"] = db.labels_

    gdf2 = gdf1.dissolve(by="cluster", aggfunc={"p2a": "count"}).rename(columns=dict(p2a="cnt"))

    gdf_coords = geopandas.GeoDataFrame(geometry=geopandas.points_from_xy(db.cluster_centers_[:, 0], db.cluster_centers_[:, 1]))
    gdf3 = gdf2.merge(gdf_coords, left_on="cluster", right_index=True).set_geometry("geometry_y")

    plt.figure(figsize=(20, 20))
    ax = plt.gca()
    gdf3.plot(ax=ax, markersize=gdf3["cnt"] / 10, column="cnt", legend=True, alpha=0.5)
    ctx.add_basemap(ax, crs="epsg:3857", source=ctx.providers.Stamen.TonerLite, alpha=0.6)

    ax.axis("off")

    if (fig_location):
        plt.savefig(fig_location)

    if (show_figure):
        plt.show()

if __name__ == "__main__":
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)

