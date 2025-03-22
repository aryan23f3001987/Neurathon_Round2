import pandas as pd
import torch
import wandb
from transformers import AutoModelForCausalLM, AutoTokenizer
import evaluate

# Initialize WandB
wandb.init(project="text-summarization-evaluation", name="Mistral-7B-Eval")

# Load ROUGE metric
rouge = evaluate.load("rouge")

# Load the pretrained Mistral model
model_path = "C:/Users/sanje/mistral_models/7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16)

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Function to generate summaries
def generate_summary(text):
    prompt = f"Summarize the following article:\n\n{text}\n\nSummary:"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    return tokenizer.decode(output[0], skip_special_tokens=True).replace(prompt, "").strip()

# Load dataset for evaluation
df = pd.read_csv("data_for_summary.csv").dropna()

# Generate summaries
df["generated_summary"] = df["text"].apply(generate_summary)

# Compute ROUGE scores
rouge_scores = rouge.compute(predictions=df["generated_summary"].tolist(), references=df["summary"].tolist(), use_stemmer=True)

# Log ROUGE scores to WandB
wandb.log({
    "ROUGE-1": rouge_scores["rouge1"],
    "ROUGE-2": rouge_scores["rouge2"],
    "ROUGE-L": rouge_scores["rougeL"]
})

# Log sample summaries
for i in range(5):  # Log 5 sample summaries
    wandb.log({
        "Sample Text": df["text"][i],
        "Ground Truth Summary": df["summary"][i],
        "Generated Summary": df["generated_summary"][i]
    })

# Save results to CSV
df.to_csv("evaluation_results.csv", index=False)
print("✅ Evaluation results saved to evaluation_results.csv")

# Finish WandB logging
wandb.finish()