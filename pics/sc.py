from pathlib import Path
import shutil
import cv2
import numpy as np

COLORS = 24

SCRIPT_DIR = Path(__file__).parent
BACKUP_DIR = SCRIPT_DIR / "pics_orig"

BACKUP_DIR.mkdir(exist_ok=True)

EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp",
    ".tif",
    ".tiff",
}

for file in SCRIPT_DIR.iterdir():
    if not file.is_file():
        continue

    if file.suffix.lower() not in EXTS:
        continue

    print(file.name)

    backup = BACKUP_DIR / file.name
    if not backup.exists():
        shutil.copy2(file, backup)

    img = cv2.imread(str(file), cv2.IMREAD_COLOR)
    if img is None:
        continue

    Z = img.reshape((-1, 3)).astype(np.float32)

    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        40,
        0.5,
    )

    _, labels, centers = cv2.kmeans(
        Z,
        COLORS,
        None,
        criteria,
        5,
        cv2.KMEANS_PP_CENTERS,
    )

    centers = np.uint8(centers)
    result = centers[labels.flatten()].reshape(img.shape)

    cv2.imwrite(str(file), result)

print("Done.")