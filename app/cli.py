import argparse
import sys
from app.inference import load_model, generate

def main():
    ap = argparse.ArgumentParser(description="Bloomed Terminal — quick CLI generator")
    ap.add_argument("-p", "--prompt", help="User prompt text. If omitted, reads from stdin.")
    ap.add_argument("--max-new", type=int, default=256)
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--top-p", type=float, default=0.95)
    args = ap.parse_args()

    prompt = args.prompt or sys.stdin.read()
    if not prompt.strip():
        print("No prompt provided.", file=sys.stderr)
        sys.exit(1)

    load_model()
    out = generate(
        [{"role": "user", "content": prompt}],
        max_new_tokens=args.max_new,
        temperature=args.temp,
        top_p=args.top_p,
    )
    print(out)

if __name__ == "__main__":
    main()
