"""
SemanticMatch demo using a JSON FAQ dataset.

This script:
- loads questions and answers from data/samples/faq.json
- lets you choose a domain (support, hr, education, all)
- builds a SemanticMatcher
- allows you to type questions and see the top-K semantic matches
"""

from src.matcher import SemanticMatcher
from src.data_loader import load_faq_json


def choose_domain():
    print("Available domains:")
    print("  1) support")
    print("  2) hr")
    print("  3) education")
    print("  4) all")
    choice = input("Select a domain (1–4, default = all): ").strip()

    mapping = {
        "1": "support",
        "2": "hr",
        "3": "education",
        "4": "all",
        "": "all",
    }
    return mapping.get(choice, "all")


def main():
    print("=== SemanticMatch Demo (FAQ from JSON, Top-K) ===")

    domain = choose_domain()
    print(f"\nLoading FAQ data for domain: {domain!r}...\n")

    questions, answers = load_faq_json("data/samples/faq.json", domain=domain)

    matcher = SemanticMatcher(questions, metadata=answers)

    print("Type a question (or 'quit' to exit):")

    while True:
        user_query = input("\nYour question: ").strip()
        if user_query.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        result = matcher.match(user_query, top_k=3)

        print("\nBest match summary:")
        print(f"  Best score:        {result['best_score']:.4f}")
        print(f"  Above threshold?   {result['meets_threshold']}")

        print("\nTop matches:")
        for i, m in enumerate(result["matches"], start=1):
            print(f"  #{i}")
            print(f"    Question: {m['question']}")
            print(f"    Answer:   {m['metadata']}")
            print(f"    Score:    {m['score']:.4f}")
        print("-" * 50)


if __name__ == "__main__":
    main()