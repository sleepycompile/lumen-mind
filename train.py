import torch
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
from model import load_model_and_tokenizer
from config import Config
from accelerate import Accelerator
from utils import compute_metrics

def prepare_data(tokenizer):
    dataset = load_dataset("json", data_files=Config.DATASET_PATH, split="train")
    
    def tokenize_function(examples):
        inputs = [Config.PROMPT_TEMPLATE.format(input=ex["input"]) + ex["response"] for ex in examples]
        tokenized = tokenizer(inputs, truncation=True, max_length=Config.MAX_SEQ_LENGTH, padding="max_length")
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)
    return tokenized_dataset

if __name__ == "__main__":
    accelerator = Accelerator()
    
    model, tokenizer = load_model_and_tokenizer()
    dataset = prepare_data(tokenizer)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    
    training_args = TrainingArguments(
        output_dir=Config.OUTPUT_DIR,
        num_train_epochs=Config.NUM_EPOCHS,
        per_device_train_batch_size=Config.BATCH_SIZE,
        learning_rate=Config.LEARNING_RATE,
        fp16=True,
        save_steps=500,
        logging_steps=100,
        evaluation_strategy="steps",
        eval_steps=200,
        report_to="none"
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )
    
    with accelerator.main_process_first():
        trainer.train()
    trainer.save_model(Config.OUTPUT_DIR)
    print("Training complete. Model saved.")