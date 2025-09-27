# AntiVibe
### SAY RIP TO VIBE CODING

# Antivibe.ai VS Code Extension

🚀 **Learn to code, don't just copy-paste!** Antivibe.ai helps you understand programming concepts instead of relying on AI to write code for you.

## Features

- 🎯 **Smart Hints**: Get guided hints instead of complete solutions
- 💡 **Progressive Assistance**: Choose hint levels from conceptual nudges to implementation guidance
- 🤔 **Thought-Provoking Questions**: Learn to think like a programmer
- 📚 **Relevant Resources**: Get pointed to learning materials

## Quick Start

### Installation

1. Clone this repository
2. Open the folder in VS Code
3. Install dependencies:
```bash
npm install
```
4. Compile the extension:
```bash
npm run compile
```
5. Press `F5` to launch a new VS Code window with the extension loaded

### Usage

1. **Select code** in your editor
2. **Right-click** and choose "Antivibe: Get Hint" or use `Ctrl+Shift+H`
3. **Choose hint level**:
   - 🚀 Level 1: Conceptual nudge
   - 💡 Level 2: Algorithm suggestion  
   - 🔧 Level 3: Implementation hint
   - 🎯 Level 4: Code structure
4. **Describe your problem** when prompted
5. **Get guided hints** that help you learn!

## Development

- **Source**: `src/extension.ts`
- **Compile**: `npm run compile`
- **Watch mode**: `npm run watch`
- **Test**: Press `F5` to debug

## What's Next

- Real AI backend integration
- Code analysis features  
- Multiple programming language support
- Learning progress tracking

## Contributing

This is an early prototype! Feel free to suggest features or report issues.

---

**Remember**: The goal is understanding, not just solving! 🧠
# Antivibe.ai VS Code Extension

🚀 **Learn to code, don't just copy-paste!** Antivibe.ai helps you understand programming concepts instead of relying on AI to write code for you.

## Features

- 🎯 **Smart Hints**: Get guided hints instead of complete solutions
- 💡 **Progressive Assistance**: Choose hint levels from conceptual nudges to implementation guidance
- 🤔 **Thought-Provoking Questions**: Learn to think like a programmer
- 📚 **Relevant Resources**: Get pointed to learning materials
- 🔍 **Problem Detection**: Automatically recognizes problem types (Two Sum, Binary Search, String Reversal, etc.)

## Quick Start

### Prerequisites

- Node.js (for VS Code extension)
- Python 3.8+ (for backend server)

### Installation & Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd AntiVibe
```

2. **Setup Backend Server**
```bash
cd antivibe-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Setup VS Code Extension**
```bash
cd antivibe-ai
npm install
```

### Running the Application

1. **Start the Backend Server** (Terminal 1):
```bash
cd antivibe-backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Run the VS Code Extension** (Terminal 2):
```bash
cd antivibe-ai
npm run compile
Press F5 to launch extension development window
```

### Usage

1. **Select code** in your editor
2. **Right-click** and choose "Antivibe: Get Hint" or use `Ctrl+Shift+H`
3. **Choose hint level**:
   - 🚀 Level 1: Conceptual nudge
   - 💡 Level 2: Algorithm suggestion  
   - 🔧 Level 3: Implementation hint
   - 🎯 Level 4: Code structure
4. **Describe your problem** when prompted
5. **Get guided hints** that help you learn!

## Supported Problem Types

- **Two Sum**: Find pairs that add to target
- **Binary Search**: Search in sorted arrays  
- **String Reversal**: Reverse strings efficiently
- **General**: Fallback for other problems

## API Endpoints

- `POST /api/hint` - Get hints for your code
- `GET /api/health` - Check server status
- `GET /api/problem-types` - List supported problems

## Project Structure

```
AntiVibe/
├── antivibe-backend/     # FastAPI server
│   ├── main.py          # Server code
│   └── requirements.txt # Python dependencies
└── antivibe-ai/         # VS Code extension
    ├── src/             # TypeScript source
    └── package.json     # Extension config
```

## Development

**Backend Development:**
```bash
cd antivibe-backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Extension Development:**
```bash
cd antivibe-ai
npm run watch  # Auto-compile on changes
Press F5 to debug
```

## Troubleshooting

**Server not connecting?**
- Check if backend is running on port 8000
- Verify `curl http://localhost:8000/api/health` works
- Ensure no firewall blocking the connection

**Extension not working?**
- Check Developer Tools (Help → Toggle Developer Tools)
- Verify `npm run compile` succeeds
- Check backend server is running

## What's Next

- More problem types and algorithms
- Code analysis for better hints  
- Learning progress tracking
- Multiple programming languages

## Contributing

This is an early prototype! Feel free to suggest features or report issues.

---

**Remember**: The goal is understanding, not just solving! 🧠

*Backend server must be running for hints to work!*
