#!/usr/bin/env python3
import argparse

from data_analyzer.core import analyze_file
from data_analyzer.report import format_report, save_report_json


def main():
    parser = argparse.ArgumentParser(description="Analyze CSV/JSON datasets.")
    parser.add_argument("input", help="Input CSV or JSON file path")
    parser.add_argument("--save-json", help="Optional output report json path")
    args = parser.parse_args()

    report = analyze_file(args.input)
    print(format_report(report))
    if args.save_json:
        path = save_report_json(report, args.save_json)
        print(f"\nReport JSON saved to: {path}")


if __name__ == "__main__":
    main()
