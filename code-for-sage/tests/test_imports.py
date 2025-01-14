import sys
import os
from pathlib import Path

# Get the absolute path of the current directory
current_dir = Path(__file__).resolve().parent

# Add the current directory to Python path
sys.path.append(str(current_dir))

try:
    from src.bot.openai_handler import SageAI
    from src.bot.course_recommender import CourseRecommender
    from src.bot.personality import SAGE_PERSONALITY
    print('✅ Success: All imports are working!')
except Exception as e:
    print(f'❌ Error: {str(e)}')
    print(f'Current directory: {current_dir}')
    print(f'Python path: {sys.path}')