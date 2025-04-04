import json

with open("../results/results_summary.json", "r") as file:
	results = json.load(file)

total_correct = sum(r['correct'] for r in results)
total_false_positives = sum(r['false_positives'] for r in results)
total_false_negatives = sum(r['false_negatives'] for r in results)

percision = total_correct / (total_correct + total_false_positives) if (total_correct + total_false_positives) > 0 else 0 
recall = total_correct / (total_correct + total_false_negatives) if (total_correct + total_false_negatives) > 0 else 0 
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0 

print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1_score:.2f}")

