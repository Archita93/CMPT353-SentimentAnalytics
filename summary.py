from transformers import pipeline
import pandas as pd
from multiprocessing import Pool
from transformers import AutoTokenizer, BartForConditionalGeneration

model_bart_cnn = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
tokenizer_bart_cnn = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer_distilbart = pipeline('summarization')
summarizer_falconai = pipeline("summarization", model="Falconsai/text_summarization")

def summarize(text, tokenizer, model, max_length=15000):
    input_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
    generated_ids = model.generate(input_ids=input_ids, num_beams=2, max_length=max_length, repetition_penalty=2.5, length_penalty=1.0)
    preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
    return preds[0]

def summary(text):
    try:
        # Generate summaries using all three models
        distil_summary = summarize(text, tokenizer_bart_cnn, model_bart_cnn, max_length=15000)
        falcons_summary = summarizer_falconai(text, max_length=1000, min_length=30, do_sample=False)
        bart_summary = summarizer_distilbart(text)

        # Return summaries as a tuple
        print(distil_summary)
        print(falcons_summary)
        print(bart_summary)

        return distil_summary, falcons_summary[0]['summary_text'], bart_summary[0]['summary_text']
    except Exception as e:
        # Handle exceptions gracefully
        print(f"An error occurred: {e}")
        return None, None, None


# Read the CSV in chunks
data = pd.read_csv("news_data_all.csv")

data[["Distil_Summary", "Falcons_Summary", "Bart_Summary"]] = data["News Article Content"].apply(lambda x: pd.Series(summary(x)))
data.to_csv("final_summ.csv", index=False)


