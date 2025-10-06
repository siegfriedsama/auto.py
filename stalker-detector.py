#!/usr/bin/env python3
# stalker_detector.py
# Fake "stalker detector" terminal output — rescans with simple "scan again" prompt.

import random
import time
import shutil
import sys
import os
import re

# ANSI color helpers
CSI = "\033["
RESET = CSI + "0m"
BOLD = CSI + "1m"
GREEN = CSI + "32m"
YELLOW = CSI + "33m"
CYAN = CSI + "36m"
MAGENTA = CSI + "35m"
DIM = CSI + "2m"

def color(text, code):
    return f"{code}{text}{RESET}"

# Name pool (anime + fantasy girls)
NAMES = [
    "Airi Kamisato","Yume Hanabira","Rin Aozora","Hikari Tsukino","Mio Kanzaki",
    "Ayaka Hoshimura","Sayuri Minazuki","Kanna Yukishiro","Arisa Fujimoto","Nozomi Takahara",
    "Haruka Amane","Rika Shion","Mei Kuronami","Satsuki Inoue","Nami Aizawa",
    "Kaori Itsuka","Luna Kisaragi","Chisato Hayami","Yuki Nanase","Eri Hinomoto",
    "Eluria Mizuhane","Sylphine Aratama","Kiyomi Raizel","Lirien Tsukihana","Amaya Seraphine",
    "Riona Akatsuki","Yuika Draviel","Ashera Kurogiri","Natsume Velaria","Kairi Solenne"
]

def terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def strip_ansi(s):
    return re.sub(r'\x1b\[[0-9;]*m', '', s)

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def header():
    w = terminal_width()
    title_text = "STALKER DETECTOR - SCAN RESULTS"
    signature = "Made with Siegfried Samà 🥐🥐🥐"
    title = color(title_text, GREEN + BOLD)
    sig_colored = color(signature, DIM)
    pad = max(0, (w - len(strip_ansi(title))) // 2)
    pad_sig = max(0, (w - len(signature)) // 2)
    print(" " * pad + title)
    print(" " * pad_sig + sig_colored)
    print()

def fake_scan_sequence():
    msgs = [
        "Initializing stalker-detector v1.04 ...",
        "Reading local device vibes ...",
        "Contacting Termux subsystem ...",
        "Cross-referencing presence cache ...",
        "Analyzing profile aura signatures ..."
    ]
    for m in msgs:
        print(color(m, CYAN))
        time.sleep(0.55 + random.random()*0.7)
    print(color("\nScan complete.\n", GREEN + BOLD))
    time.sleep(0.3)

def generate_results(count=20, style='1x'):
    pool = NAMES[:]
    random.shuffle(pool)
    picked = pool[:count]
    results = []
    for name in picked:
        if style == '1x':
            views = 1 if random.random() < 0.7 else random.choice([2,3,4,5,7])
        elif style == 'dramatic':
            views = int(max(1, (random.random()**1.2) * 50))
            if random.random() < 0.12:
                views += random.randint(20,80)
        else:
            views = random.randint(1, 12)
            if random.random() < 0.08:
                views += random.randint(5, 35)
        results.append((name, views))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def render_results(results, use_x=True):
    idx_w = len(str(len(results)))
    name_col_w = max(len(n) for n,_ in results) + 1
    for i, (name, views) in enumerate(results, 1):
        num = str(i).rjust(idx_w)
        name_field = name.ljust(name_col_w)
        view_text = f"{views}x" if use_x else f"{views} views"
        if i == 1:
            print(f"{CSI}33m{num}.{RESET} {CSI}35;1m{name_field}{RESET} - {CSI}33;1m{view_text}{RESET}")
        elif i <= 5:
            print(f"{CSI}33m{num}.{RESET} {CSI}35m{name_field}{RESET} - {CSI}36m{view_text}{RESET}")
        else:
            print(f"{CSI}33m{num}.{RESET} {name_field} - {CSI}2m{view_text}{RESET}")

def scan_once(style='1x', count=20):
    header()
    fake_scan_sequence()
    results = generate_results(count=count, style=style)
    render_results(results, use_x=True)

def interactive_loop():
    style = '1x'
    count = 20
    while True:
        clear_terminal()
        scan_once(style=style, count=count)
        # only prompt text: "scan again"
        try:
            choice = input("scan again").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice == 'q':
            break
        # any other input (including empty Enter) -> rescan (mix results)
        # loop continues

def main():
    try:
        interactive_loop()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)

if __name__ == "__main__":
    main()
