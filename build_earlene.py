#!/usr/bin/env python3
"""Build Earlene Smith transaction row matching native app typography exactly."""

from PIL import Image, ImageDraw, ImageFont
import numpy as np

ORIG = "/home/ubuntu/.cursor/projects/workspace/assets/c59ee67c-8ad8-4057-8a43-dfbfdd4251b2.jpg"
OUT = "/workspace/earlen-smith-transfer.jpg"
OUT_COPY = "/workspace/output/earlen-smith-transfer.jpg"

ROW1 = (1370, 1545)  # ChatGPT row to replace
FONT_BOLD = "/workspace/Roboto-Bold.ttf"
FONT_REG = "/workspace/Roboto-Regular.ttf"

# Sampled from reference history image (credit amounts)
GREEN = (57, 121, 100)
NAME_COLOR = (51, 51, 51)
DATE_COLOR = (136, 136, 136)

# Measured from original row1 (ChatGPT)
NAME_Y = 48
NAME_X = 41
TARGET_NAME_H = 33
TARGET_AMT_H = 35
AMT_Y = 70
DATE_Y = 107


def text_height(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def fit_font(draw, text, font_path, target_h, weight="bold", lo=20, hi=60):
    best_size, best_font, best_h = lo, None, 0
    for size in range(lo, hi + 1):
        font = ImageFont.truetype(font_path, size)
        h = text_height(draw, text, font)
        if h <= target_h:
            best_size, best_font, best_h = size, font, h
        else:
            break
    return best_font, best_size, best_h


def erase_rect(img, x1, y1, x2, y2, color=(255, 255, 255)):
    draw = ImageDraw.Draw(img)
    draw.rectangle([x1, y1, x2, y2], fill=color)


def main():
    img = Image.open(ORIG).convert("RGB")
    y1, y2 = ROW1
    row_h = y2 - y1

    # Use native row pixels as background (badge, separators, spacing)
    native_row = img.crop((0, y1, img.width, y2))

    # Erase only text regions on the row copy
    erase_rect(native_row, 35, 42, 900, 88)    # merchant name
    erase_rect(native_row, 620, 62, 900, 112)  # amount + USD
    erase_rect(native_row, 215, 100, 500, 148) # date (keep pending badge on left)

    draw = ImageDraw.Draw(native_row)

    name_font, name_size, name_h = fit_font(
        draw, "Earlene Smith", FONT_BOLD, TARGET_NAME_H
    )
    draw.text((NAME_X, NAME_Y), "Earlene Smith", fill=NAME_COLOR, font=name_font)

    # Amount number (bold-ish weight like native debit amounts)
    amt_font, amt_size, amt_h = fit_font(
        draw, "2,854.00", FONT_REG, TARGET_AMT_H, lo=24, hi=55
    )
    amt_bbox = draw.textbbox((0, 0), "2,854.00", font=amt_font)
    amt_w = amt_bbox[2] - amt_bbox[0]

    # USD label smaller (~68% of amount height)
    usd_target = max(18, int(TARGET_AMT_H * 0.68))
    usd_font, usd_size, usd_h = fit_font(
        draw, " USD", FONT_REG, usd_target, lo=14, hi=40
    )
    usd_bbox = draw.textbbox((0, 0), " USD", font=usd_font)
    usd_w = usd_bbox[2] - usd_bbox[0]

    total_w = amt_w + usd_w
    amt_x = img.width - 41 - total_w
    draw.text((amt_x, AMT_Y), "2,854.00", fill=GREEN, font=amt_font)
    draw.text((amt_x + amt_w, AMT_Y + (amt_h - usd_h)), " USD", fill=GREEN, font=usd_font)

    date_font, date_size, date_h = fit_font(
        draw, "Sep 4, 2026", FONT_REG, 36, lo=20, hi=50
    )
    draw.text((241, DATE_Y), "Sep 4, 2026", fill=DATE_COLOR, font=date_font)

    img.paste(native_row, (0, y1))
    img.save(OUT, quality=95)
    img.save(OUT_COPY, quality=95)

    # Build comparison strip
    compare = Image.new("RGB", (img.width, row_h * 3), "white")
    compare.paste(img.crop((0, y1, img.width, y2)), (0, 0))
    compare.paste(img.crop((0, 1545, img.width, 1720)), (0, row_h))
    compare.paste(img.crop((0, 1720, img.width, 1895)), (0, row_h * 2))
    compare.save("/workspace/output/compare_rows.jpg", quality=95)

    print("Saved:", OUT)
    print(f"Fonts: name={name_size}px (h={name_h}), amt={amt_size}px (h={amt_h}), usd={usd_size}px, date={date_size}px")


if __name__ == "__main__":
    main()
