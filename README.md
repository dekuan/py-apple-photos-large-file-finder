# Apple Photos Large File Finder

Find and manage large files inside the Apple Photos app on macOS. This project provides two main functionalities:

1. **Tagging large files into a dedicated album**
2. **Exporting large file metadata to a CSV file**

Unlike traditional disk scanners, this project uses Apple's official **PhotoKit** framework to read metadata directly from the Photos library database instead of enumerating local files. This ensures compatibility with iCloud-only assets and libraries using **Optimize Mac Storage**.

---

## Project Structure

```
apple-photos-large-file-finder/
├── src/
│   ├── large_files_tag_to_album.py       # Tag top large files into the 'LargeFileFinder' album
│   └── large_files_export_to_csv.py      # Export top large files metadata to CSV
├── README.md
└── LICENSE
```

> Both scripts operate independently. You can run either one depending on your workflow.

---

## Features

- Analyze assets directly from the macOS Photos app
- Works with iCloud Photos
- Compatible with **Optimize Mac Storage**
- Detect large photos and videos
- Two distinct workflows:
  - Tag top large files into a dedicated album (`LargeFileFinder`)
  - Export top large files metadata to CSV (`largest_photos.csv`)
- Supports Live Photos, RAW, HEIF, videos, and edited assets
- No direct filesystem scanning required

---

## Requirements

- macOS 13+ recommended
- Apple Silicon or Intel Mac
- Python 3.11+
- Apple Photos app
- Photos library must be configured as the **System Photo Library**

---

## Installation

Clone the repository:

```bash
git clone https://github.com/dekuan/py-apple-photos-large-file-finder.git
cd apple-photos-large-file-finder
```

Install dependencies:

```bash
python3 -m pip install -U pyobjc
```

Or install only the required frameworks:

```bash
python3 -m pip install pyobjc-framework-Photos pyobjc-framework-Cocoa
```

---

## macOS Permissions

macOS requires explicit permission to access the Photos library. Without it, scripts may return zero assets.

1. Open **System Settings → Privacy & Security → Photos**
2. Allow access for your terminal or IDE (Terminal, iTerm2, VS Code, etc.)
3. Ensure your Photos library is the **System Photo Library**:
   - Open Photos app → Settings → General → "Use as System Photo Library"

> ⚠️ Without Full Photos access, tagging or exporting assets may fail.

---

## Scripts & Usage

### 1️⃣ Tag top large files into a dedicated album

**File:** `src/large_files_tag_to_album.py`

Finds the top 1000 largest assets in your Photos library and tags them into a dedicated album called `LargeFileFinder`. Already tagged assets are skipped to avoid duplicates.

```bash
python3 src/large_files_tag_to_album.py
```

**Actual example output:**

```
Reading Photos assets...
Found 168303 assets in the Photos library.
Processed 1000/168303 assets...
Processed 2000/168303 assets...
...
Processed 167000/168303 assets...
Processed 168000/168303 assets...

Top 1000 largest assets:
   1.   13.68 GB  ScreenRecording_12-08-2024 21-51-06_1.mp4
   2.   11.84 GB  VID_20241006_202959.mp4
   3.   11.73 GB  RPReplay_Final1696922715.MP4
   ...
  19.    6.62 GB  RPReplay_Final1697954875-2.MP4
  20.    6.51 GB  RPReplay_Final1700027646.MP4

Adding assets to album: LargeFileFinder
No new assets to add. Album already contains these assets: LargeFileFinder

Done.
```

---

### 2️⃣ Export top large files metadata to CSV

**File:** `src/large_files_export_to_csv.py`

Finds the top 1000 largest assets in your Photos library and exports their metadata to a CSV file called `largest_photos.csv`.

```bash
python3 src/large_files_export_to_csv.py
```

**Actual example output:**

```
Reading Photos assets...
Found 168303 assets in the Photos library.
Processed 1000/168303 assets...
Processed 2000/168303 assets...
...
Processed 166000/168303 assets...
Processed 168000/168303 assets...
Sorting assets by size...
Writing to CSV file...

Top largest assets:

   1.   13.68 GB  ScreenRecording_12-08-2024 21-51-06_1.mp4
   2.   11.84 GB  VID_20241006_202959.mp4
   3.   11.73 GB  RPReplay_Final1696922715.MP4
   5.   10.63 GB  RPReplay_Final1722636238-1.mov
   ...
  20.    6.51 GB  RPReplay_Final1700027646.MP4

Done!
CSV file created: largest_photos.csv
```

**CSV columns include:**

| Field      | Description               |
| ---------- | ------------------------- |
| size_bytes | Raw size in bytes         |
| size_human | Human-readable size       |
| filename   | Original filename         |
| width      | Asset width               |
| height     | Asset height              |
| duration   | Video duration in seconds |
| created    | Creation date             |
| id         | Photos asset identifier   |

---

## Quick Usage Summary

```bash
# Tag largest files into the dedicated album
python3 src/large_files_tag_to_album.py

# Export largest files metadata to CSV
python3 src/large_files_export_to_csv.py
```

> ✅ Both scripts process the top 1000 largest assets by default. You can adjust the `LIMIT` constant in each script if needed.

---

## Technical Notes

- Uses **PhotoKit** (`PHAsset` and `PHAssetResource`) via PyObjC bridge
- File sizes are obtained using `resource.valueForKey_("fileSize")`
  - Apple does not provide a public API for asset file size, especially for iCloud-only assets
  - This KVC-based method is widely used and works reliably on modern macOS
- Top 1000 largest assets are used by default; scripts are configurable

---

## Limitations

- Extremely large libraries may take several minutes to process
- File size retrieval relies on undocumented KVC access
- Future macOS updates may change PhotoKit behavior
- iCloud-only resources may report partial metadata

---

## Future Plans

- GUI interface for selecting and tagging assets
- Duplicate photo detection
- Live Photo and HEIF/RAW analysis
- Smart filtering and advanced reporting
- Storage heatmaps for the Photos library

---

## License

MIT License

---

## Disclaimer

This project is not affiliated with Apple Inc.

Apple Photos, PhotoKit, macOS, and iCloud are trademarks of Apple Inc.
