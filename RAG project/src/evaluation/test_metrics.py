from metrics import calculate_metrics


retrieved = [
    "A",
    "B",
    "C",
    "D",
    "E"
]

relevant = [
    "A",
    "C",
    "F"
]


metrics = calculate_metrics(
    retrieved,
    relevant,
    k=5
)


print("=" * 50)
print("METRICS TEST")
print("=" * 50)

print(f"Precision@5: {metrics['precision']:.2f}")
print(f"Recall@5:    {metrics['recall']:.2f}")
print(f"F1@5:        {metrics['f1']:.2f}")
print(f"Hit Rate@5:  {metrics['hit_rate']:.2f}")
print(f"MRR@5:       {metrics['mrr']:.2f}")