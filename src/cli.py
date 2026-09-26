import argparse
import json

from src.rag import answer


def main():
    parser = argparse.ArgumentParser(description="NetOps GenAI Assistant CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask", help="Ask a grounded question against the runbook corpus")
    ask.add_argument("question")

    args = parser.parse_args()

    if args.command == "ask":
        result = answer(args.question)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
