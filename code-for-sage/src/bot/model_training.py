"""
Model fine-tuning and training utilities for Sage
"""

import json
import os
from typing import List, Dict
from openai import OpenAI
from datetime import datetime

class ModelTrainer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.training_data_path = "data/training/"
        
    def prepare_training_data(self, conversations: List[Dict]) -> str:
        """Convert conversations to JSONL format for fine-tuning"""
        output_path = f"{self.training_data_path}training_data_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        with open(output_path, 'w') as f:
            for conv in conversations:
                training_example = {
                    "messages": [
                        {"role": "system", "content": "You are Sage, a career mentor bot."},
                        {"role": "user", "content": conv["user_input"]},
                        {"role": "assistant", "content": conv["bot_response"]}
                    ]
                }
                f.write(json.dumps(training_example) + '\n')
                
        return output_path
    
    async def start_fine_tuning(self, training_file_path: str):
        """Start fine-tuning job with OpenAI"""
        try:
            # Upload the training file
            with open(training_file_path, 'rb') as f:
                training_file = self.client.files.create(
                    file=f,
                    purpose='fine-tune'
                )
            
            # Create fine-tuning job
            job = self.client.fine_tuning.jobs.create(
                training_file=training_file.id,
                model="gpt-3.5-turbo",
                hyperparameters={
                    "n_epochs": 3
                }
            )
            
            return {
                'status': 'success',
                'job_id': job.id,
                'model': job.model
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def get_fine_tuning_status(self, job_id: str):
        """Check status of fine-tuning job"""
        try:
            job = self.client.fine_tuning.jobs.retrieve(job_id)
            return {
                'status': job.status,
                'trained_tokens': job.trained_tokens,
                'error': job.error
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
