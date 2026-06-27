# Multi-Agent Code Feature Extraction & Documentation Suite 🚀

An enterprise-grade, asynchronous multi-agent orchestration framework built in Python to analyze, dissect, and document complex codebases. Powered by LLM analysis, it automatically maps software architecture, detects languages, measures code quality, flags security risks, and builds beautiful documentation wrappers (including automated Doxygen UX enhancements).

---

## 🗺️ Documentation Index
To make this documentation easy to navigate for your engineering and product teams, it is divided into specialized modules:
* **[Architecture & Component Breakdown](ARCHITECTURE.md)**: Deep dive into the thread-safe <code>Crew</code> framework, custom Directed Acyclic Graph (DAG) executor, and agent responsibilities.
* **[Getting Started & Configuration](GETTING_STARTED.md)**: System prerequisites, environment setup, execution commands, and output analysis.
* **[Development & Extension Guide](DEVELOPMENT.md)**: How to modify existing agents, implement custom analysis layers, and extend the pipeline.

---

## 🛠️ Application & System Features
The suite provides a dual-layer approach to software analysis: **System Orchestration** and **Application-level Extractors**.

### ⚙️ System-Level Features
* **Parallel Execution DAG**: Uses <code>networkx</code> to map agent dependencies and validate that the pipeline forms a Directed Acyclic Graph, avoiding deadlocks before triggering runs.
* **Asynchronous Processing**: Leverages a <code>ThreadPoolExecutor</code> to execute independent agents concurrently, optimizing overall speed.
* **Thread-Safe Shared Context**: Employs a synchronized <code>threading.Lock</code> across all agents to allow safe concurrent reads and writes to the global execution context.
* **Smart Result Caching**: Implements localized JSON persistence (<code>load_existing_result</code>) to cache LLM queries, avoiding redundant API costs and allowing instant workflow resumes.

### 📊 Application-Level Extractors
| Agent Name | Core Extracted Feature | Output / Objective |
| :--- | :--- | :--- |
| **ProjectTreeAnalyzer** | Structural Layout Detection | Identifies layout style (modular, layered, monolithic) and maps directory hierarchy. |
| **LanguageDetector** | Multi-lingual Classification | Detects code/config/markup languages, standards, and estimates codebase size. |
| **CodeArchitectureAnalyzer** | Structural Code Binding | Extracts AST semantics, creates function/class call graphs, maps code elements. |
| **QualityAnalyzer** | Quantitative Quality Metrics | Scores code, test coverage gaps, performance bottlenecks, and technical debt. |
| **MDDocumentationMaker** | Document Generation Pipeline | Compiles final markdown summaries using asset registries and template engines. |
| **DoxygenDocumentationUXBuilder**| UX Front-end Architect | Generates optimized HTML templates, stylesheets, and custom landing pages. |

---

## 🧱 Architectural Topology

<pre>
       [ ProjectTreeAnalyzer ]      [ LanguageDetector ]      [ BuildSystemDetector ]
                  \                          |                         /
                   \                         |                        /
                 [------------------- MDTemplateAnalyzer -------------------]
                                             |
                                 [ MDDocumentationMaker ]
                                             |
                            [ DoxygenDocumentationUXBuilder ]
</pre>

---

## 📄 License
This suite is distributed under the **BSD Free License**. You are completely free to modify, integrate, distribute, and commercialize this software under the terms of the BSD license, provided that original copyright notices are retained.