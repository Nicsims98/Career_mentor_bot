import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.config import THEME, CHATBOT_CONFIG

def test_config():
    print("\nRunning Configuration Tests...")
    
    # Test 1: Check if all required theme colors exist
    required_colors = ['primary', 'secondary', 'accent', 'background', 'text']
    missing_colors = [color for color in required_colors if color not in THEME]
    
    if not missing_colors:
        print("✅ All theme colors present")
    else:
        print("❌ Missing colors:", missing_colors)

    # Test 2: Check if all chatbot settings exist
    required_settings = ['max_context_length', 'max_response_length', 'temperature']
    missing_settings = [setting for setting in required_settings if setting not in CHATBOT_CONFIG]
    
    if not missing_settings:
        print("✅ All chatbot settings present")
    else:
        print("❌ Missing settings:", missing_settings)

    # Test 3: Verify color format (should be hex codes starting with #)
    invalid_colors = [color for color in THEME.values() if not color.startswith('#')]
    
    if not invalid_colors:
        print("✅ All color formats valid")
    else:
        print("❌ Invalid color formats:", invalid_colors)

    print("\nFull Configuration:")
    print("\nTheme Colors:")
    for key, value in THEME.items():
        print(f"  {key}: {value}")
    
    print("\nChatbot Settings:")
    for key, value in CHATBOT_CONFIG.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_config()