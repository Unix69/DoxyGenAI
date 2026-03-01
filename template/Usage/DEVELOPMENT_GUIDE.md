<div align="left">

  <h1>🧑‍💻 Developer Guide</h1>

  <br>

  <!-- Badges -->
  <div align="bottom">
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/graphs/contributors">
      <img src="https://img.shields.io/github/contributors/Unix69/EmbeddedDocsTemplates" alt="contributors" />
    </a>
    <a href="">
      <img src="https://img.shields.io/github/last-commit/Unix69/EmbeddedDocsTemplates" alt="last update" />
    </a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/network/members">
      <img src="https://img.shields.io/github/forks/Unix69/EmbeddedDocsTemplates" alt="forks" />
    </a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/stargazers">
      <img src="https://img.shields.io/github/stars/Unix69/EmbeddedDocsTemplates" alt="stars"/>
    </a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/issues/">
      <img src="https://img.shields.io/github/issues/Unix69/EmbeddedDocsTemplates" alt="open issues" />
    </a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/blob/master/LICENSE.md">
      <img src="https://img.shields.io/github/license/Unix69/EmbeddedDocsTemplates.svg" alt="license" />
    </a>
  </div>

  <p>
    This <b>Developer Guide</b> explains how to extend, customize, and maintain the internal structure of the <b>EmbeddedDocsTemplates</b> project.
    It provides guidance on the template architecture, build system, APIs, namespaces, file conventions, and Doxygen integration.
  </p>

</div>

<br><br>

<a name="table-of-contents"></a>

### 📓 Table of Contents
- [Development Overview](#development-overview)
- [Environment Setup](#environment-setup)
- [Code Structure](#code-structure)
- [API Development](#api-development)
- [Namespace Management](#namespace-management)
- [How To](#how-to)
- [Other Guides](#other-guides)
- [FAQ](#faq)

<br><br>

<a name="development-overview"></a>

# Development Overview 🧠

[Table of Contents](#table-of-contents)

The README Template is designed to support:

- Multi-level documentation (User, Admin, Developer)
- Version tracking under <code>/Version</code>
- Feature/API/Namespace documentation
- Automatic rendering using Doxygen
- HTML + Markdown synchronization
- Modular architecture

The development workflow involves modifying:

- Markdown content (<code>/Usage</code>, <code>/Version</code>)
- Doxygen config (<code>Doxyfile</code>)
- Template assets (<code>header.html</code>, <code>footer.html</code>, <code>stylesheet.css</code>)
- Build scripts (<code>Makefile</code>)

All contributions should preserve template coherence and consistent linking across documents.

<br><br>

<a name="environment-setup"></a>

# Environment Setup ⚙️

To work on the template structure, set up your environment as follows:

1. Clone the repository:  
   <code>git clone https://github.com/Unix69/EmbeddedDocsTemplates.git</code>

2. Enter the template directory:  
   <code>cd EmbeddedDocsTemplates</code>

3. Ensure you have the required tools:  
   - Doxygen  
   - Graphviz (optional, for diagrams)  
   - GNU Make  

4. Build the documentation locally:  
   <code>make build</code>  
   <code>make doc</code>

5. Open:  
   <code>docs/html/index.html</code>

This environment allows you to test changes to Markdown files, navigation links, Doxygen tags, and HTML templates.

<br><br>

<a name="code-structure"></a>

# Code Structure 🧩

The template follows a clear structure:

| Path | Purpose |
|------|---------|
| <code>/Usage/</code> | Guides: User, Admin, Developer |
| <code>/Version/</code> | Versioning, changelog, fixes |
| <code>/Images/</code> | Logos and documentation assets |
| <code>/include/</code> | Example headers for API/namespace docs |
| <code>/src/</code> | Sample source files |
| <code>/docs/</code> | Generated Doxygen output |
| <code>/Makefile</code> | Build automation |
| <code>Doxyfile</code> | Documentation engine configuration |

### Naming conventions
- Markdown files: <code>SECTION_NAME.md</code>  
- Features: <code>FEATURE_*.md</code>  
- API files: <code>api_*.md</code>  
- Namespaces: <code>namespace_*.md</code>  

### Developer responsibilities
- Maintain consistency between Markdown and Doxygen HTML  
- Ensure links <code>data-github</code> and <code>data-doxygen</code> work correctly  
- Add new documentation in the correct folder  
- Keep Makefile rules synchronized with repository structure  

<br><br>

<a name="api-development"></a>

# API Development 🧠

Developers extending API documentation should:

1. Add or update header files inside <code>/include/</code>.
2. Use proper Doxygen tags:
   - <code>@file</code>  
   - <code>@brief</code>  
   - <code>@param</code>  
   - <code>@return</code>  
   - <code>@namespace</code>  
   - <code>@api</code> (custom tag used in template)
3. Reflect changes in Markdown under <code>/Usage</code> or <code>/Version</code> when appropriate.
4. Regenerate documentation:  
   <code>make doc</code>
   

API sections will automatically appear under:
<code>docs/html/modules.html</code>  
or  
<code>docs/html/namespaces.html</code>

<br><br>

<a name="namespace-management"></a>

# Namespace Management 📦

The template lets you document C/C++ namespaces in a structured way.

### To add a namespace:

1. Define it in source or header (<code>/src</code> or <code>/include</code>).
2. Add a Markdown section under <code>/Usage</code> or <code>/Version</code>.
3. Document it using Doxygen:  
   <code>/** @namespace myNamespace */</code>
4. Ensure references use the interactive Doxygen mapping:  
   <code>data-doxygen="namespace_myNamespace.html"</code>
5. Rebuild documentation:  
   <code>make doc</code>

Namespaces automatically generate interlinked HTML pages.

<br><br>

<a name="how-to"></a>

# How To 🛠️

[Table of Contents](#table-of-contents)

<a name="how-to-build"></a>
## How to build the project (Template build)
1. Clone the template  
   <code>git clone ...</code>  
2. Build assets  
   <code>make build</code>  
3. Generate documentation  
   <code>make doc</code>  
4. Browse  
   <code>docs/html/index.html</code>

<br>

<a name="how-to-integrate-feature"></a>
## How to integrate new features
1. Create a new Feature Markdown file  
   <code>/Usage/FEATURE_*.md</code>  
2. Add Doxygen links  
3. If needed, add example code under <code>/src</code>  
4. Update <code>PROJECT.md</code> or <code>USECASES.md</code>  
5. Run  
   <code>make doc</code>

<br>

<a name="how-to-extend-api"></a>
## How to extend APIs
1. Add new header in <code>/include</code>  
2. Document API elements with Doxygen  
3. Update API-related Markdown  
4. Rebuild documentation  
   <code>make doc</code>

<br><br>

<a name="other-guides"></a>

# Other Guides 📚

| Role | Reference | Description |
|------|------------|-------------|
| 📘 **User Guide** | <span class="md-link" data-github="Usage/USER_GUIDE.md" data-doxygen="md_Usage_USER_GUIDE.html"><a href="USER_GUIDE.md"><b>USER_GUIDE.md</b></a></span> | End-user operations |
| 🧑‍💼 **Admin Guide** | <span class="md-link" data-github="Usage/ADMINISTRATOR_GUIDE.md" data-doxygen="md_Usage_ADMINISTRATOR_GUIDE.html"><a href="ADMINISTRATOR_GUIDE.md"><b>ADMINISTRATOR_GUIDE.md</b></a></span> | Configuration & maintenance |

<br><br>

<a name="faq"></a>

# FAQ ❓

<b>Q:</b> How do I add new documentation modules?  
<b>A:</b> Add a Markdown file in <code>/Usage</code> or <code>/Version</code> and run <code>make doc</code>.

<br>

<b>Q:</b> How do I customize the HTML output?  
<b>A:</b> Modify <code>header.html</code>, <code>footer.html</code>, or <code>stylesheet.css</code>.

<br>

<b>Q:</b> Where do I define new APIs or namespaces?  
<b>A:</b> Under <code>/include</code> with proper Doxygen annotations.

<br><br>

<br>
<br>

# Contact Us ☎️

For more information about the README Template → <span class="md-link" data-github="CONTACT_US.md" data-doxygen="md_CONTACT_US.html"><a href="CONTACT_US.md"><b>Contact Page</b></a></span>

<br><br>
</div>
