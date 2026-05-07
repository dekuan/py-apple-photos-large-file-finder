#!/usr/bin/env python3

from datetime import datetime

from Photos import (
    PHAsset,
    PHAssetResource,
    PHPhotoLibrary,
    PHAssetCollection,
    PHAssetCollectionTypeAlbum,
    PHAssetCollectionSubtypeAlbumRegular,
    PHAssetCollectionChangeRequest,
)

LIMIT = 1000
ALBUM_NAME = "LargeFileFinder"


def format_size(size):
    size = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


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


def find_album(album_name):
    collections = PHAssetCollection.fetchAssetCollectionsWithType_subtype_options_(
        PHAssetCollectionTypeAlbum,
        PHAssetCollectionSubtypeAlbumRegular,
        None,
    )

    for i in range(collections.count()):
        collection = collections.objectAtIndex_(i)
        if str(collection.localizedTitle()) == album_name:
            return collection

    return None


def create_album(album_name):
    def change_block():
        PHAssetCollectionChangeRequest.creationRequestForAssetCollectionWithTitle_(
            album_name
        )

    success, error = PHPhotoLibrary.sharedPhotoLibrary().performChangesAndWait_error_(
        change_block,
        None,
    )

    if not success:
        raise RuntimeError(f"Failed to create album: {error}")

    return find_album(album_name)


def get_existing_asset_ids_in_album(album):
    existing_ids = set()
    assets = PHAsset.fetchAssetsInAssetCollection_options_(album, None)
    for i in range(assets.count()):
        asset = assets.objectAtIndex_(i)
        existing_ids.add(str(asset.localIdentifier()))
    return existing_ids


def add_assets_to_album_without_duplicates(assets, album_name):
    if not assets:
        print("No assets to add.")
        return

    album = find_album(album_name)
    if album is None:
        print(f"Creating album: {album_name}")
        album = create_album(album_name)

    if album is None:
        raise RuntimeError(f"Could not find or create album: {album_name}")

    existing_ids = get_existing_asset_ids_in_album(album)

    new_assets = [
        asset for asset in assets if str(asset.localIdentifier()) not in existing_ids
    ]

    if not new_assets:
        print(
            f"No new assets to add. Album already contains these assets: {album_name}"
        )
        return

    def change_block():
        request = PHAssetCollectionChangeRequest.changeRequestForAssetCollection_(album)
        request.addAssets_(new_assets)

    success, error = PHPhotoLibrary.sharedPhotoLibrary().performChangesAndWait_error_(
        change_block,
        None,
    )

    if not success:
        raise RuntimeError(f"Failed to add assets to album: {error}")

    print(f"Added {len(new_assets)} new assets to album: {album_name}")


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
            total_size += get_file_size(r)

            try:
                filename = r.originalFilename()
                if filename:
                    filenames.append(str(filename))
            except Exception:
                pass

        result.append(
            {
                "size_bytes": total_size,
                "size_human": format_size(total_size),
                "filename": " | ".join(filenames),
                "_asset": asset,
            }
        )

        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1}/{total} assets...")

    if not result:
        print("No Photos assets found.")
        return

    result.sort(key=lambda x: x["size_bytes"], reverse=True)
    result = result[:LIMIT]

    top_assets = [item["_asset"] for item in result]

    print(f"\nTop {len(top_assets)} largest assets:")
    for idx, item in enumerate(result[:20], 1):
        print(f'{idx:>4}. {item["size_human"]:>10}  {item["filename"]}')

    print(f"\nAdding assets to album: {ALBUM_NAME}")
    add_assets_to_album_without_duplicates(top_assets, ALBUM_NAME)

    print("\nDone.")


if __name__ == "__main__":
    main()
