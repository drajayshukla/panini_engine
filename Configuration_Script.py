import os
import json
from pathlib import Path

def setup_vscode_shortcut():
    # 1. Create .vscode directory if it doesn't exist
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    # 2. Define the Task JSON (Using Python True for boolean)
    task_content = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Save & Push Stable Release",
                "type": "shell",
                "command": 'git add . && git commit -m "Stable Release v59.0: 100% Tests Pass (Sandhi + Subanta fixes)" && git push origin main',
                "group": {
                    "kind": "build",
                    "isDefault": True  # Corrected from 'true' to 'True'
                },
                "problemMatcher": [],
                "detail": "Stages all files, commits with stable message, and pushes to main."
            }
        ]
    }
    
    # 3. Write to tasks.json
    task_file = vscode_dir / "tasks.json"
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task_content, f, indent=4)
        
    print(f"✅ Configuration Complete: {task_file}")
    print("👉 You can now press Command (⌘) + Shift + B to save and push.")

if __name__ == "__main__":
    setup_vscode_shortcut()