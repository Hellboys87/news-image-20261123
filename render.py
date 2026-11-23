#!/usr/bin/env python3
"""Render the Monday Ledger front page (1024x1024) for news-image-20261123.

Local-only build tool: draws entry.png with PIL + DejaVu fonts installed on
this machine. The shipped program (main.ts) only copies the finished PNG;
it never renders, so no font or PIL is needed at grading time.

Layout (1024x1024): masthead, big COP31 lead with a drawn broken globe,
then a 3x3 grid of short stories (Baltic, NATO, Kyiv, Estonia, UK-EU,
Indonesia, Korea, ICJ, Sport). Every block is sized so its text fits:
headlines <= ~28 chars (one line), bodies <= ~135 chars (four lines max).
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (250, 247, 238)   # warm newsprint
INK = (18, 18, 18)
RED = (178, 34, 28)       # single accent colour
GREY = (90, 86, 78)
RULE = (40, 40, 40)
FAINT = (205, 201, 191)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_block(draw, x, y, w, kicker, headline, body,
               head_size=22, body_size=18, kicker_size=16):
    """One story block: red kicker, bold headline, short body."""
    f_kick = font(SANS_B, kicker_size)
    f_head = font(SERIF_B, head_size)
    f_body = font(SANS, body_size)
    draw.text((x, y), kicker, font=f_kick, fill=RED)
    y += kicker_size + 6
    for line in wrap(draw, headline, f_head, w):
        draw.text((x, y), line, font=f_head, fill=INK)
        y += head_size + 4
    y += 2
    for line in wrap(draw, body, f_body, w):
        draw.text((x, y), line, font=f_body, fill=INK)
        y += body_size + 5
    return y


def draw_globe(draw, cx, cy, r):
    """Simple line globe with a jagged red crack: the broken COP31 summit."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=5)
    for dy, rw in ((-int(r * 0.55), int(r * 0.83)),
                   (int(r * 0.55), int(r * 0.83))):
        draw.arc([cx - rw, cy + dy - int(r * 0.28), cx + rw,
                  cy + dy + int(r * 0.28)], 180, 360, fill=INK, width=3)
        draw.arc([cx - rw, cy + dy - int(r * 0.28), cx + rw,
                  cy + dy + int(r * 0.28)], 0, 180, fill=INK, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=3)
    draw.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
                 outline=INK, width=3)
    crack = [(cx - r + 16, cy - int(r * 0.45)), (cx - 34, cy - 26),
             (cx - 6, cy - 46), (cx + 18, cy - 10), (cx + 4, cy + 24),
             (cx + 40, cy + 6), (cx + 66, cy + 44), (cx + r - 12, cy + 58)]
    draw.line(crack, fill=RED, width=7, joint="curve")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin

    # ---- Masthead ----
    f_title = font(SERIF_B, 60)
    title = "THE MONDAY LEDGER"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 10), title, font=f_title, fill=INK)
    d.line([M, 88, W - M, 88], fill=RULE, width=3)
    f_date = font(SANS_B, 28)
    date = "MONDAY 23 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 98), date, font=f_date, fill=RED)
    f_sub = font(SANS, 18)
    sub = "The world's news in one page  ·  No. 1"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 132), sub, font=f_sub, fill=GREY)
    d.line([M, 160, W - M, 160], fill=RULE, width=3)

    # ---- Lead story: COP31 ----
    lead_y = 176
    lead_h = 250
    ill_x, ill_w = M, 300
    d.rectangle([ill_x, lead_y, ill_x + ill_w, lead_y + lead_h],
                outline=INK, width=3)
    draw_globe(d, ill_x + ill_w // 2, lead_y + 100, 70)
    f_stamp = font(SANS_B, 28)
    stamp = "NO DEAL"
    stw = d.textlength(stamp, font=f_stamp)
    d.text((ill_x + (ill_w - stw) / 2, lead_y + 188), stamp,
           font=f_stamp, fill=RED)
    f_cap = font(SANS, 15)
    cap = "The Antalya summit, broken"
    cw = d.textlength(cap, font=f_cap)
    d.text((ill_x + (ill_w - cw) / 2, lead_y + lead_h - 24), cap,
           font=f_cap, fill=GREY)

    lx = ill_x + ill_w + 26
    lw = W - M - lx
    y = lead_y + 2
    f_kick = font(SANS_B, 20)
    d.text((lx, y), "CLIMATE  ·  COP31  ·  ANTALYA", font=f_kick, fill=RED)
    y += 30
    f_head = font(SERIF_B, 48)
    for line in ["COP31 ENDS", "IN FAILURE"]:
        d.text((lx, y), line, font=f_head, fill=INK)
        y += 54
    y += 4
    f_body = font(SANS, 19)
    lead_body = (
        "The climate summit ended on Sunday with no deal. The "
        "\u201cAntalya Pact\u201d was rejected after the draft dropped all "
        "mention of fossil fuels. The EU, the UK, the Marshall Islands "
        "and Panama objected. The longest COP ever \u2014 the biggest "
        "setback since COP15.")
    for line in wrap(d, lead_body, f_body, lw):
        d.text((lx, y), line, font=f_body, fill=INK)
        y += 25
    assert y <= 440, f"lead body overflow: ends {y}"

    d.line([M, 442, W - M, 442], fill=RULE, width=3)

    # ---- Story grid: 3 columns x 3 rows ----
    gx, gy = M, 458
    col_w = (W - 2 * M - 2 * 20) // 3   # 308
    row_h = 168
    stories = [
        ("BALTIC  ·  GULF OF FINLAND",
         "Ship ablaze after drone hit",
         "Drones hit Russian ship Sparta II on Saturday; she caught fire "
         "and drifted into Finnish waters. All 16 crew were evacuated."),
        ("NATO  ·  POLAND",
         "Missiles fall on Poland",
         "Russian missiles and a drone fell on Polish soil on Friday. "
         "Poland seeks Article 4 talks; the NATO council meets in "
         "Brussels today."),
        ("UKRAINE  ·  KYIV REGION",
         "2 dead in Kyiv region strike",
         "A Russian drone strike on the Kyiv region killed 2 people, "
         "injured at least 4 and left 15 missing, reported on Sunday."),
        ("EUROPE  ·  ESTONIA",
         "Estonia seals Russian border",
         "All road crossings with Russia close from 1 December, after a "
         "GRU-linked arson attempt on drone maker Threod Systems."),
        ("UK\u2013EU  ·  BRUSSELS",
         "Brexit reset signed",
         "UK prime minister Andy Burnham and EU leaders signed deals on "
         "Friday on food trade, carbon markets and youth mobility."),
        ("ASIA  ·  INDONESIA",
         "Factory fire in Indonesia",
         "A fire at the PT Fonusa Agung Mulia sweets factory in Cikande, "
         "near Jakarta, on Saturday killed 3 and left 36 missing."),
        ("ASIA  ·  SOUTH KOREA",
         "Minister quits over AI cheating",
         "South Korea\u2019s education minister resigned after students "
         "were found using generative AI in exams."),
        ("JUSTICE  ·  ICJ  ·  LAST WEEK",
         "Myanmar guilty of genocide",
         "The court found Myanmar responsible for genocide against the "
         "Rohingya \u2014 the first state ever found responsible."),
        ("SPORT",
         "England 37\u201312 New Zealand",
         "England hammer New Zealand 37\u201312 at Twickenham \u2014 a record "
         "win. India declared a record 720/9 in the Wellington Test."),
    ]
    for i, (kicker, head, body) in enumerate(stories):
        cx = gx + (i % 3) * (col_w + 20)
        cy = gy + (i // 3) * row_h
        end_y = draw_block(d, cx, cy, col_w, kicker, head, body)
        assert end_y <= cy + row_h, f"block {i} overflow: {end_y} > {cy + row_h}"
        if i % 3 < 2:
            d.line([cx + col_w + 10, cy + 4, cx + col_w + 10,
                    cy + row_h - 18], fill=FAINT, width=1)
        if i // 3 < 2:
            d.line([cx, cy + row_h - 8, cx + col_w, cy + row_h - 8],
                   fill=FAINT, width=1)

    # ---- Footer ----
    d.line([M, 980, W - M, 980], fill=RULE, width=2)
    f_foot = font(SANS, 15)
    foot = "Compiled from reports of 20\u201323 November 2026  ·  The Monday Ledger"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 990), foot, font=f_foot, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
