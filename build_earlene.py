#!/usr/bin/env python3
"""Build Earlene Smith transaction row matching the provided reference layout."""

from pathlib import Path

from PIL import Image

BASE = Path("/workspace/earlen-smith-transfer.jpg")
REFERENCE = Path(
    "/home/ubuntu/.cursor/projects/workspace/assets/"
    "01a2ac68-0589-4598-aaeb-cdc1e2678aa9.jpg"
)
REFERENCE_COPY = Path("/workspace/reference-earlene-row.jpg")
OUT = Path("/workspace/earlen-smith-transfer.jpg")
OUT_COPY = Path("/workspace/output/earlen-smith-transfer.jpg")
ROW_PREVIEW = Path("/workspace/output/earlen_row_final.jpg")
COMPARE = Path("/workspace/output/compare_rows.jpg")

ROW = (1372, 1545)


def main():
    if not BASE.exists():
        raise FileNotFoundError(f"Base screenshot not found: {BASE}")

    ref_path = REFERENCE if REFERENCE.exists() else REFERENCE_COPY
    if not ref_path.exists():
        raise FileNotFoundError(
            "Reference row image not found. Expected one of:\n"
            f"  - {REFERENCE}\n"
            f"  - {REFERENCE_COPY}"
        )

    img = Image.open(BASE).convert("RGB")
    reference = Image.open(ref_path).convert("RGB")

    y1, y2 = ROW
    row_h = y2 - y1
    row_w = img.width

    scaled_row = reference.resize((row_w, row_h), Image.Resampling.LANCZOS)

    result = img.copy()
    result.paste(scaled_row, (0, y1))
    result.save(OUT, quality=95)
    result.save(OUT_COPY, quality=95)
    scaled_row.save(ROW_PREVIEW, quality=95)

    compare = Image.new("RGB", (row_w, row_h * 3), "white")
    compare.paste(scaled_row, (0, 0))
    compare.paste(result.crop((0, 1545, row_w, 1720)), (0, row_h))
    compare.paste(result.crop((0, 1720, row_w, 1895)), (0, row_h * 2))
    compare.save(COMPARE, quality=95)

    print("Saved:", OUT)
    print("Layout:")
    print("  Earlene Smith")
    print("  Aug 20, 2026")
    print("  7,905.50 USD")
    print("  Amount: 500.00 USD")


if __name__ == "__main__":
    main()
