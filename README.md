# Agentic_army

Agentic_army is a modular Python framework designed for building, testing, and deploying agent-based systems for research, automation, and information retrieval tasks. The project provides a flexible architecture for creating specialized agents, integrating tools, and managing data sources, with a focus on research workflows and document analysis.

## Features

- **Agent Architecture:** Easily create and extend agents for research, synthesis, and writing tasks.
- **Tool Integration:** Plug-and-play tools for document loading, search, and custom agent actions.
- **Data Management:** Organized data storage, including support for arXiv and other research sources.
- **Jupyter Support:** Example notebooks for interactive experimentation and testing.

## Project Structure

```
agents_test.ipynb         # Example/test notebook for agent workflows
limit.py                  # Utility or configuration module
main.py                   # Main entry point for running agents
test.ipynb                # Additional notebook for testing
agents/                   # Core agent implementations
    __init__.py
    research_agent.py     # Main research agent logic
data/                     # Data storage (e.g., arXiv papers)
    arxiv/
        files/
tools/                    # Tool modules for agents
    __init__.py
    agent_tools.py        # General agent tools
    document_loaders.py   # Document/data loading utilities
    search_tools.py       # Search and retrieval tools
README.md                 # Project documentation
```

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd Agentic_army
   ```

2. **Install dependencies:**
   (Create a virtual environment and install required packages. If requirements.txt is missing, install standard packages like `requests`, `pandas`, etc., as needed by your agents.)
   ```sh
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the main script:**
   ```sh
   python main.py
   ```

4. **Explore Notebooks:**
   Open `agents_test.ipynb` or `test.ipynb` in Jupyter for interactive demos.

## Usage

- **Develop new agents:** Add Python files in the `agents/` directory and register them in `main.py`.
- **Add tools:** Implement new tools in `tools/` and import them into your agents.
- **Data sources:** Place or sync research data (e.g., arXiv files) in `data/arxiv/files/`.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or documentation improvements.

## License

This project is licensed under the MIT License.

## Contact

For questions or collaboration, contact [Varun Kumar Foujdhar](mailto:your.email@example.com).
