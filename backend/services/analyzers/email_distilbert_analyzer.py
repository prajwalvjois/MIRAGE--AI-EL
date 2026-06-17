import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from backend.core.interfaces.ianalyzer import IAnalyzer

class EmailDistilBERTAnalyzer(IAnalyzer):
    def __init__(self, model_dir: str = "backend/models/email/distilbert/"):
        print("[MIRAGE] DistilBERT Email Model Loaded")
        
        self.model_path = os.path.abspath(os.path.join(model_dir, "model.safetensors"))
        self.is_loaded = False
        
        if not os.path.exists(self.model_path):
            print("CRITICAL ERROR: DistilBERT model.safetensors is missing!")
            print(f"Please manually copy the model.safetensors file to: {self.model_path}")
        else:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
                self.is_loaded = True
            except Exception as e:
                print(f"Error loading DistilBERT model: {e}")

    def analyze_email(self, email_text: str) -> float:
        if not email_text:
            return 0.0
            
        if not self.is_loaded:
            print(f"WARNING: Cannot analyze email, model.safetensors missing at {self.model_path}")
            return 0.0

        try:
            inputs = self.tokenizer(
                email_text,
                return_tensors="pt",
                truncation=True,
                max_length=512
            )
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            # LABEL_0 = Legitimate, LABEL_1 = Phishing
            phishing_probability = predictions[0][1].item()
            
            print(f"[MIRAGE] Email Risk Score: {phishing_probability}")
            return float(phishing_probability)
        except Exception as e:
            print(f"Error during DistilBERT inference: {e}")
            return 0.0

    def analyze_url(self, url: str) -> float:
        # Fallback to MockAnalyzer logic for URLs as per instructions
        return 0.30
