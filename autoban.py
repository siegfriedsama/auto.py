#!/usr/bin/env python3
# fb_auto_ban_demo_realistic.py
# HARMLSS LOCAL DEMO — dramatic terminal output only.
# Shows Followers: 0 for effect. Does NOT contact Facebook or any network.

import sys, os, time, random, shutil
from datetime import datetime

# ANSI color codes
CSI = "\033["
RESET = CSI + "0m"
BOLD = CSI + "1m"
GREEN = CSI + "32m"
YELLOW = CSI + "33m"
CYAN = CSI + "36m"
MAGENTA = CSI + "35m"
RED = CSI + "31m"
DIM = CSI + "2m"

def c(text, col): return f"{col}{text}{RESET}"
def clear(): os.system("cls" if os.name=="nt" else "clear")
def term_w():
    try: return shutil.get_terminal_size().columns
    except: return 80

# UI helpers
def progress(task, total=36, speed=0.035):
    width = min(50, max(24, term_w()//3))
    sys.stdout.write(c(f"{task}: ", CYAN))
    sys.stdout.flush()
    for i in range(total+1):
        filled = int(i/total * width)
        bar = "[" + "#"*filled + "-"*(width-filled) + "]"
        pct = int(i/total*100)
        sys.stdout.write(f"\r{c(task+':', CYAN)} {bar} {pct:3d}%")
        sys.stdout.flush()
        time.sleep(speed + random.random()*0.02)
    sys.stdout.write("\n")

def spinner(d=1.2, label="processing"):
    chars="|/-\\"
    end=time.time()+d; i=0
    while time.time()<end:
        sys.stdout.write(f"\r{c(label+':', CYAN)} {chars[i%4]} ")
        sys.stdout.flush(); i+=1; time.sleep(0.07)
    sys.stdout.write("\r" + " "*(len(label)+8) + "\r")

def center_line(text):
    return text.center(term_w())

# content
HEADER = "FACEBOOK AUTO BAN"
DEMOTAG = "(SUNOG ACCOUNT)"
SIGN = "Made with Siegfried Samà 🥐🥐🥐"

BACKEND_MESSAGES = [
    "Resolving profile metadata",
    "Gathering public posts & attachments",
    "Scanning comments & flagged content",
    "Cross-referencing reports",
    "Matching policy violations",
    "Preparing enforcement decision",
    "Queuing for automated enforcement",
    "Applying enforcement payload"
]

OUTCOMES = [
    ("Account suspended", RED),
    ("Temporary restriction applied (simulated)", YELLOW),
    ("Content removed, account intact", MAGENTA),
    ("No actionable violation found — dismissed (simulated)", GREEN)
]

def show_header():
    clear()
    # Header, then DEMO tag, then signature (Made with ...)
    print(c(center_line(HEADER), GREEN + BOLD))
    print(c(center_line(DEMOTAG), DIM))
    print(c(center_line(SIGN), DIM))
    print()

def fake_profile_lookup(url):
    progress("Validating URL format", total=18, speed=0.028)
    spinner(0.9, "fetching public metadata")
    # dramatic: followers set to 0
    name = random.choice(["Kagumi Chan"])
    followers = 0
    created = f"{random.randint(2010,2021)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    print(c(f"Found profile: {name}", YELLOW))
    # make zero followers stand out visually
    print(c(f"Followers: {followers}", RED + BOLD))
    print(c(f"Account created: {created}", DIM))
    print()

def simulate_flow(target):
    steps = random.sample(BACKEND_MESSAGES, k=5)
    for s in steps:
        progress(s, total=random.randint(20,36), speed=0.03 + random.random()*0.03)
        if random.random() < 0.5:
            print(c(" > extracting attachments...", DIM))
            time.sleep(0.12 + random.random()*0.35)
    print()
    progress("Submitting case to moderation engines", total=26, speed=0.035)
    spinner(0.8, "queuing")
    progress("Finalizing enforcement action", total=28, speed=0.04)

def decide_outcome():
    r = random.random()
    if r < 0.70: return OUTCOMES[0]
    elif r < 0.88: return OUTCOMES[1]
    elif r < 0.97: return OUTCOMES[2]
    else: return OUTCOMES[3]

def save_log(target, result):
    fn = f"fb_demo_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(fn, "w", encoding="utf-8") as f:
            f.write("FACEBOOK AUTO BAN\n")
            f.write(f"Target: {target}\n")
            f.write(f"Result: {result}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
            f.write("NOTE: LOCAL SIMULATION ONLY — NO NETWORK ACTIONS PERFORMED.\n")
        print(c(f"Local log saved: {fn}", DIM))
    except Exception as e:
        print(c(f"Failed to save log: {e}", RED))

def main():
    show_header()
    while True:
        try:
            target = input(c("Enter Facebook profile URL (or 'q' to quit): ", DIM)).strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not target:
            continue
        if target.lower() in ("q","quit","exit"):
            print(c("Bye.", DIM)); break

        fake_profile_lookup(target)
        confirm = input(c("Proceed with enforcement? (y/N): ", DIM)).strip().lower()
        if confirm not in ("y","yes"):
            print(c("Cancelled. Returning to menu.\n", DIM)); continue

        show_header()
        print(c(f"Targeting: {target}", YELLOW))
        simulate_flow(target)
        outcome_text, color = decide_outcome()
        print()
        print(c(center_line("=== ENFORCEMENT RESULT ==="), BOLD))
        print()
        print(c(f"Result: {outcome_text}", color + BOLD))
        print(c("Reason: Matched multiple policy clauses.", DIM))
        print()
        # always show demo tag again for clarity
        print(c(center_line(""), DIM))
        save = input(c("Save local log? (y/N): ", DIM)).strip().lower()
        if save in ("y","yes"): save_log(target, outcome_text)
        again = input(c("\nRun another? (Enter to continue, q to quit): ", DIM)).strip().lower()
        if again in ("q","quit","exit"): break
        show_header()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + c("Interrupted. Exiting.", DIM))
