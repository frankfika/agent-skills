#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a clear 16:9 comparison card for X/Twitter posts.
"""

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1600
HEIGHT = 900


def load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "C:/Windows/Fonts/msyh.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    value: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_gap: int = 10,
) -> int:
    x, y = xy
    lines: list[str] = []
    for paragraph in value.splitlines() or [""]:
        line = ""
        for char in paragraph:
            trial = line + char
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = char
        if line:
            lines.append(line)

    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        current_y += font.size + line_gap
    return current_y


def draw_bullets(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    items: Iterable[str],
    color: str,
    max_width: int,
) -> int:
    body_font = load_font(31)
    current_y = y
    for item in items:
        draw.ellipse((x, current_y + 10, x + 14, current_y + 24), fill=color)
        current_y = draw_wrapped(
            draw,
            (x + 34, current_y),
            item,
            body_font,
            "#202020",
            max_width=max_width,
        )
        current_y += 22
    return current_y


def build_card(args: argparse.Namespace) -> None:
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (WIDTH, HEIGHT), "#f7f5ef")
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((70, 70, 1530, 830), radius=34, fill="#fffdf8", outline="#ddd7c9", width=2)
    draw.rectangle((70, 70, 1530, 186), fill="#101820")
    draw.rounded_rectangle((70, 70, 1530, 830), radius=34, outline="#ddd7c9", width=2)

    draw.text((120, 104), args.title, font=load_font(58), fill="#ffffff")
    draw.text((1040, 118), args.tagline, font=load_font(34), fill="#d6ff8d")

    draw.rounded_rectangle((120, 245, 755, 705), radius=24, fill="#e8f7f1", outline="#b8d8cc", width=2)
    draw.rounded_rectangle((845, 245, 1480, 705), radius=24, fill="#f1ecff", outline="#cfc3ee", width=2)

    draw.text((165, 290), args.left_title, font=load_font(48), fill="#0c5b45")
    draw.text((890, 290), args.right_title, font=load_font(48), fill="#5a3f9c")

    draw_bullets(draw, 165, 375, args.left, "#178a69", 500)
    draw_bullets(draw, 890, 375, args.right, "#7657c7", 500)

    if args.footer:
        draw.rounded_rectangle((205, 742, 1395, 795), radius=16, fill="#101820")
        draw_wrapped(draw, (250, 754), args.footer, load_font(30), "#ffffff", max_width=1100, line_gap=8)

    image.save(output, quality=95)
    print(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an X/Twitter comparison card.")
    parser.add_argument("--title", required=True, help="Main card title.")
    parser.add_argument("--tagline", default="不是替代，是分工", help="Top-right tagline.")
    parser.add_argument("--left-title", required=True, help="Left column title.")
    parser.add_argument("--left", action="append", required=True, help="Left column bullet. Can be repeated.")
    parser.add_argument("--right-title", required=True, help="Right column title.")
    parser.add_argument("--right", action="append", required=True, help="Right column bullet. Can be repeated.")
    parser.add_argument("--footer", default="", help="Bottom summary line.")
    parser.add_argument("--output", required=True, help="Output PNG path.")
    return parser.parse_args()


if __name__ == "__main__":
    build_card(parse_args())
