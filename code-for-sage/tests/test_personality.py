import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.bot.personality import SAGE_PERSONALITY

def test_sage_personality():
    print("\nTesting Sage's Personality Configuration:")
    print(f"\n🤖 Name: {SAGE_PERSONALITY['name']}")
    print("\n✨ Traits:")
    for key, value in SAGE_PERSONALITY['traits'].items():
        print(f"  • {key}: {value}")
    
    print("\n🎨 Brand Colors:")
    for key, value in SAGE_PERSONALITY['colors'].items():
        print(f"  • {key}: {value}")
    
    print("\n👋 Introduction Message:")
    print(SAGE_PERSONALITY['introduction'])

if __name__ == "__main__":
    test_sage_personality()