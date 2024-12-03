# Alice

<div align="center">
  <img src="./arts/alice-4.jpg" alt="Alice Banner" width="20%" />
</div>

## 🚀 Quick Start

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 20+](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

### Manually Start Service

```bash
# Clone the repo
git clone https://github.com/aliceailabs/alice
cd alice

# Install dependencies
pip install -r requirements.txt
cp .env.example .env
```

### Edit the .env file

### Start 

```bash
# will be listening on port 8000 by default
uvicorn app.main:app --reload
```
