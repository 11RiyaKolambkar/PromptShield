import pandas as pd

df = pd.read_csv("results_all.csv")

print("=== LEAKS (naive bot) ===")
leaks = df[(df.level == "1_naive") & (df.success)]
for _, r in leaks.iterrows():
    print(f"\n[{r.category}] {r.prompt}\n-> {r.reply[:300]}")

print("\n\n=== SAMPLE REPLIES from 2_with_rules (should be refusals) ===")
for _, r in df[df.level == "2_with_rules"].sample(6, random_state=1).iterrows():
    print(f"\n[{r.category}] {r.prompt}\n-> {r.reply}")