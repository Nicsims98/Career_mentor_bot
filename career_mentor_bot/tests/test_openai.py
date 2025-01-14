import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.bot.openai_handler import SageAI

async def test_sage_ai():
    sage = SageAI()
    
    # Test basic career question
    test_input = "What skills do I need to become a data scientist?"
    
    print("\nTesting Sage's Career Advice:")
    print(f"\nUser Question: {test_input}")
    
    response = await sage.get_career_advice(test_input)
    print("\nSage's Response:")
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_sage_ai())