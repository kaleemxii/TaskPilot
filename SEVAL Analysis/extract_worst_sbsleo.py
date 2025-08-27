import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent / "Data"
INPUT_FILENAME = "Demo - 1 - SEVAL Metrics for analysis.csv"
OUTPUT_FILENAME = "output.csv"

INPUT_PATH = DATA_DIR / INPUT_FILENAME
OUTPUT_PATH = Path(__file__).parent / OUTPUT_FILENAME  # same location as Answer.md per instruction

CONTROL_COL = "sbsleo_detail_control"
TREAT_COL = "sbsleo_detail_treatment"

UTTERANCE_COL = "utterance"
SEGMENT_COL = "segment 2"  # dataset uses a space; instruction said segment2
DEBUGLINK_COL = "DebugLink"

def to_float(val):
    if val is None:
        return None
    val = val.strip()
    if val == "":
        return None
    try:
        return float(val)
    except ValueError:
        return None

def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input CSV not found at {INPUT_PATH}")

    with INPUT_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("Input CSV is empty")

        # Map column name to index (case sensitive)
        idx = {name: i for i, name in enumerate(header)}
        required = [UTTERANCE_COL, SEGMENT_COL, DEBUGLINK_COL, CONTROL_COL, TREAT_COL]
        missing = [c for c in required if c not in idx]
        if missing:
            raise KeyError(f"Missing required columns: {missing}")

        rows = []
        for row in reader:
            if not row or len(row) < len(header):
                # allow short / empty lines
                continue
            control_v = to_float(row[idx[CONTROL_COL]])
            treat_v = to_float(row[idx[TREAT_COL]])
            # Only consider rows where both values present
            if control_v is None or treat_v is None:
                continue
            delta = treat_v - control_v  # negative means treatment worse
            rows.append({
                UTTERANCE_COL: row[idx[UTTERANCE_COL]],
                SEGMENT_COL: row[idx[SEGMENT_COL]],
                DEBUGLINK_COL: row[idx[DEBUGLINK_COL]],
                CONTROL_COL: control_v,
                TREAT_COL: treat_v,
                "_delta": delta,
            })

    # Sort by delta ascending (most negative first = maximally worse)
    rows.sort(key=lambda r: r["_delta"])  # ascending
    top50 = rows[:50]

    # Write output with only requested columns
    out_fields = [UTTERANCE_COL, SEGMENT_COL, DEBUGLINK_COL, CONTROL_COL, TREAT_COL]
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(out_fields)
        for r in top50:
            writer.writerow([r[c] for c in out_fields])

    print(f"Wrote {len(top50)} rows to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
