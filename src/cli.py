import argparse
import csv
import json

from src.agent import extract_site_id, triage
from src.rag import answer


def batch_triage(input_path: str, output_path: str):
    with open(input_path) as f:
        incidents = [line.strip() for line in f if line.strip()]

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["incident_text", "site_id", "severity", "likely_cause", "sources"])
        for incident in incidents:
            result = triage(incident)
            writer.writerow([incident, extract_site_id(incident) or "", result.severity, result.likely_cause, ";".join(result.sources)])


def main():
    parser = argparse.ArgumentParser(description="NetOps GenAI Assistant CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask", help="Ask a grounded question against the runbook corpus")
    ask.add_argument("question")

    batch = sub.add_parser("batch-triage", help="Triage a file of incidents (one per line) into a CSV")
    batch.add_argument("input_file")
    batch.add_argument("output_file")

    args = parser.parse_args()

    if args.command == "ask":
        result = answer(args.question)
        print(json.dumps(result, indent=2))
    elif args.command == "batch-triage":
        batch_triage(args.input_file, args.output_file)
        print(f"Wrote results to {args.output_file}")


if __name__ == "__main__":
    main()
