#!/usr/bin/env python


import re
import argparse
import os
import logging
import json

# import cv2 as cv
from PIL import Image
import pytesseract


def gen_calendar(event_conf, out_path):
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\n"
    for c, t, r, s in event_conf:
        date, start, end = t
        ics_content += f"""BEGIN:VEVENT
SUMMARY:{c}
DTSTART;TZID=Asia/Shanghai:{date}T{start.replace(":", "")}00
DTEND;TZID=Asia/Shanghai:{date}T{end.replace(":", "")}00
LOCATION:{r} 座位号: {s}
END:VEVENT
"""
    ics_content += "END:VCALENDAR"

    with open(out_path, 'w') as f:
        f.write(ics_content)


def parse_text(texts):
    """Pair infos"""
    lines = texts.splitlines()
    lines = [line.replace(" ", "") for line in lines if line.strip()]
    time_idxs = []
    seat_idxs = []
    room_idxs = []
    cur_idxs = []
    for i, line in enumerate(lines):
        if re.match(r"\d{4}-\d{2}-\d{2}", line):
            time_idxs.append(i)
            room_idxs.append(i + 1)
            cur_idxs.append(i - 1)
        if re.match(r"座位", line):
            seat_idxs.append(i)
    seats = [lines[i] for i in seat_idxs]
    rooms = [lines[i] for i in room_idxs]
    curs = [lines[i] for i in cur_idxs]
    times = []
    date_re = re.compile(r"\d{4}-\d{2}-\d{2}")
    time_re = re.compile(r"\d{2}:\d{2}")
    for i in time_idxs:
        date = date_re.search(lines[i]).group()
        start, end = time_re.findall(lines[i])
        times.append((date, start, end))
    conf = [
        (c, t, r, s)
        for c, t, r, s in zip(curs, times, rooms, seats)
    ]
    return conf


def ocr(img_path):
    # img = cv.imread(img_path)
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = Image.open(img_path)
    gray = img.convert('L')
    text = pytesseract.image_to_string(gray, lang="chi_sim")
    return text


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", "-i", type=str, default="exams.jpg", help="Path to the image file")
    parser.add_argument("--out_path", "-o", type=str, default="output", help="Path to the output ics file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print more info")
    parser.add_argument("--tesseract_path", "-t", type=str, default="/usr/bin/tesseract",
                        help="Path to the tesseract executable")
    args = parser.parse_args()
    if not args.out_path.endswith(".ics"):
        outfolder = True
    else:
        outfolder = False
    if outfolder:
        if not os.path.exists(args.out_path):
            os.makedirs(args.out_path)
        fn_base = os.path.basename(args.image_path).split(".")[0]
        args.out_path = os.path.join(args.out_path, fn_base + ".ics")
    return args


def main(opt):
    if not os.path.exists(opt.image_path):
        print(f"Error: Image file not found: {opt.image_path}")
        return 1
    if opt.verbose:
        logging.basicConfig(level=logging.INFO)
    pytesseract.pytesseract.tesseract_cmd = opt.tesseract_path
    logging.info(f"Using tesseract at {opt.tesseract_path}")
    texts = ocr(opt.image_path)
    logging.info(f"OCR result: {texts}")
    conf = parse_text(texts)
    cf = json.dumps(conf, ensure_ascii=False, indent=2)
    logging.info(f"Parse result: {cf}")
    gen_calendar(conf, opt.out_path)
    logging.info(f"Calendar file generated at {opt.out_path}")
    return 0


if __name__ == "__main__":
    exit(main(parse_opt()))
