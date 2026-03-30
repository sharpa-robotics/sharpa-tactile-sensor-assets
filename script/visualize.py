import argparse
import os

import numpy as np
import matplotlib.pyplot as plt


def plot_group(ax, points: np.ndarray, normals: np.ndarray, title: str, color: str):
    ax.scatter(points[:, 0], points[:, 1], points[:, 2],
               s=0.3, color=color, alpha=0.6)

    ax.quiver(
        points[:, 0], points[:, 1], points[:, 2],
        normals[:, 0], normals[:, 1], normals[:, 2],
        color=color, alpha=0.5, linewidth=0.5,
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_aspect("equal")
    ax.set_title(title)


GROUPS = [
    {"key": "4F", "points": "tactileSensor_map_4F_point.npy", "normals": "tactileSensor_map_4F_normal.npy", "color": "tab:blue"},
    {"key": "TH", "points": "tactileSensor_map_TH_point.npy", "normals": "tactileSensor_map_TH_normal.npy", "color": "tab:orange"},
]


def main():
    parser = argparse.ArgumentParser(description="Visualize tactile sensor points and normals")
    parser.add_argument("--path", required=True, help="Directory containing .npy files")
    parser.add_argument("--down-sample", type=int, default=8, help="Downsample factor N: keep every N-th point along each axis")
    args = parser.parse_args()
    ds = args.down_sample

    fig = plt.figure(figsize=(16, 7))

    for i, g in enumerate(GROUPS):
        pts_path = os.path.join(args.path, g["points"])
        nrm_path = os.path.join(args.path, g["normals"])
        pts = np.load(pts_path)[::ds, ::ds].reshape(-1, 3)
        nrm = np.load(nrm_path)[::ds, ::ds].reshape(-1, 3)
        print(f"{g['key']}: {pts.shape[0]} vertices (down-sample={ds})")

        ax = fig.add_subplot(1, len(GROUPS), i + 1, projection="3d")
        plot_group(ax, pts, nrm, g["key"], g["color"])

    fig.suptitle(f"Tactile Sensor — {args.path}", fontsize=14)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
