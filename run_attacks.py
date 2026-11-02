import pandas as pd
from chatbot import build_chatbot, leaked
from attacks import ATTACKS

RUNS = 2  # each attack is run twice, because LLM replies can vary


def run(label, **settings):
    ask = build_chatbot(**settings)
    rows = []
    for a in ATTACKS:
        for _ in range(RUNS):
            reply = ask(a["prompt"])
            rows.append({
                "level": label,
                "category": a["category"],
                "prompt": a["prompt"],
                "success": leaked(reply),
                "reply": reply,
            })
    df = pd.DataFrame(rows)
    df.to_csv(f"results_{label}.csv", index=False)
    print(f"{label}: {df.success.mean():.0%} ({df.success.sum()} of {len(df)})")
    return df


if __name__ == "__main__":
    levels = [
        run("1_naive", naive=True),
        run("2_with_rules"),
        run("3_strict_prompt", strict=True),
        run("4_strict_plus_filter", strict=True, output_filter=True),
    ]
    all_df = pd.concat(levels)
    all_df.to_csv("results_all.csv", index=False)

    print("\n=== Attack success rate by level and category ===")
    table = all_df.pivot_table(index="level", columns="category",
                               values="success", aggfunc="mean")
    table["OVERALL"] = all_df.groupby("level").success.mean()
    print((table * 100).round(0).astype(int).astype(str) + "%")