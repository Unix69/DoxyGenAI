# 🏗️ Architecture & Component Breakdown

This document outlines the software engineering design, concurrency models, and detailed components powering the multi-agent orchestration engine.

---

## 🏎️ Core Orchestration Engine

The architecture relies on an explicit separation between the execution coordinator (<code>Crew</code>) and the atomic executors (<code>Agent</code>). 

### 1. The Concurrency Wrapper (<code>Crew.py</code>)
The <code>Crew</code> class is responsible for structural verification and lifecycle coordination of all active agents.
* **DAG Verification**: Prior to run-time execution, <code>verify_dag()</code> utilizes <code>networkx</code> to perform cycle checks. If a cyclic dependency exists, it halts safely, preventing run-time deadlocks.
* **Worker Pool**: Uses <code>ThreadPoolExecutor(max_workers=max_workers)</code> to execute processing threads concurrently.
* **Reactive Loop**: An internal scheduler continuously polls active futures. When an agent satisfies its <code>depends_on</code> criteria, it is pushed straight into the thread executor thread queue.

### 2. Synchronized Isolation (<code>Agent.py</code>)
The base <code>Agent</code> class encapsulates individual LLM prompts, localized file processing, and execution states.
* **Context Locking**: Shared state manipulation is strictly isolated. The <code>self.lock</code> context element guarantees that multiple agents updating <code>crew_context["results"]</code> will not experience thread contention or data races.
* **Caching Strategy**: Prevents duplicate execution. It queries <code>load_existing_result()</code> to see if a valid <code>&lt;AgentName&gt;.json</code> is present. If found, it loads from disk and skips remote inference entirely.

---

## 🧩 Detailed Agent Dependencies & Pipeline Graph

Here is the exact dependency structure specified inside the codebase:

<pre>
1. LanguageDetector           ──┐
2. DependencyDetector         ──┤
3. CodeArchitectureAnalyzer   ──┤
4. APIAnalyzer                ──┤
5. UsageAnalyzer              ──┤  ==> All feed directly into ==>  [ MDTemplateAnalyzer ]
6. DevOpsAnalyzer             ──┤                                        │
7. SecurityPermissionAnalyzer ──┤                                        ▼
8. DocumentationAnalyzer      ──┤                              [ MDDocumentationMaker ]
9. VersioningAnalyzer         ──┤                                        │
10. QualityAnalyzer           ──┤                                        ▼
11. ProjectTreeAnalyzer       ──┤                       [ DoxygenDocumentationUXBuilder ]
12. BuildSystemDetector       ──┤
13. ProjectMetadataAnalyzer   ──┘
</pre>

### Component Deep-Dive
* **Semantic Binder**: <code>CodeArchitectureAnalyzer</code> identifies functional semantics, creates a unified call graph, and matches structural source entities with designated template goals using structured JSON payloads.
* **Quality Metrics Aggregator**: <code>QualityAnalyzer</code> orchestrates qualitative analysis over source code arrays. It filters files through a dynamic batch classifier (<code>get_file_classifier()</code>) to score Technical Debt, Test Reliability, and Performance Vulnerabilities.
* **UX Generation Factory**: <code>DoxygenDocumentationUXBuilder</code> ingests aggregated context blocks and directly crafts responsive static assets (<code>index.html</code>, <code>stylesheet.css</code>, and custom functional wrappers) inside the project destination folder.