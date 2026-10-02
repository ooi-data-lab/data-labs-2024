# OOI Data Labs Array Map - North America 
# Revised August 27, 2026

from pathlib import Path

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

OOI_ARRAYS = [
    {
        "name": "Global Station Papa",
        "lat": 49.9795,
        "lon": -144.2540,
        "text_dx": -12,
        "text_dy": 0,
        "ha": "right",
        "line_mode": "none",
    },
    {
        "name": "Regional Cabled Array",
        "lat": 45.9413,
        "lon": -129.9697,
        "text_dx": -54,
        "text_dy": -20,
        "ha": "right",
        "line_mode": "angled",
        "horiz_len_pts": 20,
    },
    {
        "name": "Coastal Endurance",
        "lat": 44.6598,
        "lon": -124.0958,
        "text_dx": -58,
        "text_dy": -48,
        "ha": "right",
        "line_mode": "angled",
        "horiz_len_pts": 20,
        # "text_gap_pts": 12,
        "marker_clear_pts": 16,
    },
    {
        "name": "Coastal Pioneer NES",
        "lat": 40.1000,
        "lon": -70.8800,
        "text_dx": 62,
        "text_dy": 4,
        "ha": "left",
        "line_mode": "angled",
        "horiz_len_pts": 22,
        "discontinued": 2022,
    },
    {
        "name": "Coastal Pioneer MAB",
        "lat": 35.9500,
        "lon": -75.1250,
        "text_dx": 62,
        "text_dy": -20,
        "ha": "left",
        "line_mode": "angled",
        "horiz_len_pts": 22,
    },
    {
        "name": "Global Irminger Sea",
        "lat": 59.9341,
        "lon": -39.4673,
        "text_dx": 12,
        "text_dy": 0,
        "ha": "left",
        "line_mode": "none",
    },
   {
        "name": "Global Argentine Basin",
        "lat": -42.5073,
        "lon": -42.8905,
        "text_dx": 16,
        "text_dy": 0,
        "ha": "left",
        "line_mode": "none",
        "discontinued": 2020,
    },
    {
        "name": "Global Southern Ocean",
        "lat": -54.0814,
        "lon": -89.6652,
        "text_dx": -16,
        "text_dy": 0,
        "ha": "right",
        "line_mode": "none",
        "discontinued": 2020,
    },
]

def draw_ooi_map(output_path: Path) -> None:
    """Create and output a map of the OOI Arrays"""
    fig = plt.figure(figsize=(14, 10), dpi=160)
    fig.patch.set_facecolor("#0b2e4e")
    ax = plt.axes(
        projection=ccrs.Orthographic(
            central_longitude=-95,
            # central_latitude=45,
        )
    )

    # ax.set_extent([-180, 0, -72, 78], crs=ccrs.PlateCarree())

    # Textured background with stronger bathy/relief contrast and darker land.
    ax.set_facecolor("#0b2e4e")
    ax.background_img(name="ne_shaded", resolution="low")
    ax.add_feature(cfeature.OCEAN.with_scale("110m"), facecolor="#072641", alpha=0.25, zorder=1)
    ax.add_feature(cfeature.LAND.with_scale("110m"), facecolor="#041a2d", alpha=0.74, zorder=2)
    ax.add_feature(cfeature.LAKES.with_scale("110m"), facecolor="#072641", alpha=0.38, zorder=2)
    ax.add_feature(cfeature.COASTLINE.with_scale("110m"), edgecolor="#2d6c9a", linewidth=0.5, zorder=3)
    ax.add_feature(cfeature.BORDERS.with_scale("110m"), edgecolor="#2d6c9a", linewidth=0.35, zorder=2)

    ax.gridlines(
        draw_labels=False,
        # xlocs=range(-180, 181, 20),
        # ylocs=[lat for lat in range(-60, 81, 15) if lat != 0],
        color="#5a89ab",
        alpha=0.35,
        linewidth=0.5,
        linestyle="--",
        zorder=3,
    )

    # Equator drawn separately so it stands out from the minor grid lines.
    ax.plot(
        [-179.9, 179.9],
        [0, 0],
        transform=ccrs.PlateCarree(),
        color="#f1f4f8",
        linewidth=0.9,
        alpha=0.55,
        zorder=3,
    )

    marker_edge = "#f5d45b"
    marker_fill = "none"
    line_color = "#f5d45b"
    text_color = "#f1f4f8"
    pts_to_px = fig.dpi / 94 #72.0
    text_gap_pts = 0
    horiz_len_pts = 18.0
    marker_clear_pts = 4.0

    for arr in OOI_ARRAYS:
        lon = arr["lon"]
        lat = arr["lat"]
        text_dx = arr["text_dx"]
        text_dy = arr["text_dy"]
        ha = arr["ha"]
        line_mode = arr.get("line_mode", "angled")
        this_horiz_len_pts = arr.get("horiz_len_pts", horiz_len_pts)
        this_text_gap_pts = arr.get("text_gap_pts", text_gap_pts)
        this_marker_clear_pts = arr.get("marker_clear_pts", marker_clear_pts)

        # Marker style: yellow ring with yellow center dot.
        ax.scatter(lon, lat, s=142, facecolors=marker_fill, edgecolors=marker_edge, linewidths=2.1, zorder=5, transform=ccrs.PlateCarree())
        ax.scatter(lon, lat, s=22, c=marker_edge, zorder=6, transform=ccrs.PlateCarree(),)

        # Optional leader lines: none for Papa/Irminger, straight for Cabled, angled for others.
        if line_mode != "none":
            marker_xy = ax.projection.transform_point(lon, lat, ccrs.PlateCarree())
            marker_disp = ax.transData.transform(marker_xy)
            if ha == "left":
                line_end_dx_pts = text_dx - this_text_gap_pts
                elbow_dx_pts = max(line_end_dx_pts - this_horiz_len_pts, this_marker_clear_pts)
            else:
                line_end_dx_pts = text_dx + this_text_gap_pts
                elbow_dx_pts = min(line_end_dx_pts + this_horiz_len_pts, -this_marker_clear_pts)

            if line_mode == "straight":
                line_disp = [
                    marker_disp,
                    (
                        marker_disp[0] + line_end_dx_pts * pts_to_px,
                        marker_disp[1] + text_dy * pts_to_px,
                    ),
                ]
            else:
                line_disp = [
                    marker_disp,
                    (
                        marker_disp[0] + elbow_dx_pts * pts_to_px,
                        marker_disp[1] + text_dy * pts_to_px,
                    ),
                    (
                        marker_disp[0] + line_end_dx_pts * pts_to_px,
                        marker_disp[1] + text_dy * pts_to_px,
                    ),
                ]

            line_data = [ax.transData.inverted().transform(p) for p in line_disp]
            ax.plot(
                [p[0] for p in line_data],
                [p[1] for p in line_data],
                color=line_color,
                linewidth=1.5,
                zorder=6,
            )

        # Labels still use display-space offsets for stable screen layout.
        ax.annotate(
            arr["name"],
            xy=(lon, lat),
            xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
            xytext=(text_dx, text_dy),
            textcoords="offset points",
            color=text_color,
            fontsize=15.5,
            fontweight="bold",
            ha=ha,
            va="center",
            zorder=7,
        )

        # Add optional Discontinued annotations
        if "discontinued" in arr:
            ax.annotate(
                f"Discontinued {arr['discontinued']}",
                xy=(lon, lat),
                xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                xytext=(text_dx, text_dy - 16),
                textcoords="offset points",
                color='yellow',
                fontsize=8,
                fontweight="bold",
                ha=ha,
                va="center",
                zorder=7,
        )

    # plt.title("OOI Arrays", color=text_color, fontsize=15, fontweight="bold", pad=8)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(output_path, bbox_inches="tight", pad_inches=.2, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    filename = Path(__file__).resolve().with_name("ooi_map_full_hemisphere.png")
    draw_ooi_map(filename)
    print(f"Saved map to: {filename}")
