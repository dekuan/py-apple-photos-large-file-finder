#!/usr/bin/env python3

from Photos import (
    PHAsset,
    PHAssetResource,
    PHPhotoLibrary,
)

from Foundation import NSObject
import csv
from datetime import datetime

LIMIT = 1000


def format_size(size):
    size = float(size)

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def nsdate_to_str(date_obj):
    if not date_obj:
        return ""

    ts = date_obj.timeIntervalSince1970()
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def get_file_size(resource):
    """
    Get the file size of a Photos asset resource.
    Works for both local and iCloud-managed assets.
    """
    try:
        size = resource.valueForKey_("fileSize")
        return int(size) if size is not None else 0
    except Exception:
        return 0


def main():
    print("Reading Photos assets...")

    assets = PHAsset.fetchAssetsWithOptions_(None)
    total = assets.count()
    print(f"Found {total} assets in the Photos library.")

    result = []

    for i in range(total):
        asset = assets.objectAtIndex_(i)
        resources = PHAssetResource.assetResourcesForAsset_(asset)

        total_size = 0
        filenames = []

        for r in resources:
            size = get_file_size(r)
            total_size += size

            try:
                filenames.append(str(r.originalFilename()))
            except Exception:
                pass

        row = {
            "size_bytes": total_size,
            "size_human": format_size(total_size),
            "filename": " | ".join(filenames),
            "width": asset.pixelWidth(),
            "height": asset.pixelHeight(),
            "duration": round(asset.duration(), 2),
            "created": nsdate_to_str(asset.creationDate()),
            "id": str(asset.localIdentifier()),
        }

        result.append(row)

        if (i + 1) % 1000 == 0:
            print(f"Processed {i+1}/{total} assets...")

    print("Sorting assets by size...")

    result.sort(key=lambda x: x["size_bytes"], reverse=True)
    result = result[:LIMIT]

    if not result:
        print("No Photos assets found.")
        print(
            "Please check your system permissions: System Settings → Privacy & Security → Photos → allow access for Terminal/iTerm/VS Code"
        )
        return

    print("Writing to CSV file...")

    with open(
        "largest_photos.csv",
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:
        writer = csv.DictWriter(f, fieldnames=result[0].keys())
        writer.writeheader()
        writer.writerows(result)

    print("\nTop largest assets:\n")
    for idx, item in enumerate(result[:20], 1):
        print(f"{idx:>4}. {item['size_human']:>10}  {item['filename']}")

    print("\nDone!")
    print("CSV file created: largest_photos.csv")


if __name__ == "__main__":
    main()
