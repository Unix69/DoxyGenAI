# 🚀 Getting Started & Configuration

Follow this comprehensive guide to configure, run, and validate your Multi-Agent Code Feature Extraction Suite.

---

## 🎛️ Prerequisites
Ensure your operational environment contains the following minimum configurations:
* **Python Engine**: Version <code>3.9</code> or higher.
* **Core Libraries**: <code>networkx</code>, <code>python-dotenv</code>, <code>openai</code> or designated LLM client libraries.
* **Git Access**: Valid credentials for <code>GitHubManager</code> interactions if analyzing remote repositories.

---

## 📦 Installation

To download the required dependencies, execute the environment installation inside your terminal:

<pre><code>pip install networkx python-dotenv openpyxl weasyprint openai</code></pre>

---

## ⚙️ Environment Configuration

Create an <code>.env</code> file inside your core <code>Agents</code> workspace folder configuration:

<pre><code>
# Core API Token Configuration
GITHUB_TOKEN=your_secure_github_personal_access_token
GITHUB_USERNAME=your_github_username

# Working Directory Context Paths
SRC_PATH=/absolute/or/relative/path/to/target/source/projects
</code></pre>

---

## ⚡ Execution

To initiate the multi-threaded code exploration pipeline, execute the main module entry point:

<pre><code>python main.py</code></pre>

### Processing Workflow Overview
1. **Context Loading**: <code>main.py</code> scans the target <code>SRC_PATH</code> environment.
2. **Thread Initialization**: Launches a background pool to parse independent structures.
3. **DAG Verification**: Evaluates agent relationship maps for safety validation.
4. **Generation Phase**: Produces structured markdown files and a dedicated static UI tree inside <code>doxygen_ui/</code>.

---

## 🧪 Testing Verification

You can easily validate the stability of the orchestration platform by setting up mock file arrays and asserting JSON generation:

<pre><code>python -m unittest discover -s tests</code></pre>

### Diagnostic Inspection Points
* **Orchestration Diagnostics**: Check output logs to ensure that <code>[Crew] DAG validated</code> and <code>[Crew] start running</code> complete without exceptions.
* **Cache Assertions**: Verify that the system successfully populates <code>crew_outputs/</code> with valid <code>&lt;AgentName&gt;.json</code> files after the initial run.