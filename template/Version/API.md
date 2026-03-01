<h1> 🧩 API </h1>

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

🏗️ <span class="md-link"
         data-github="../PROJECT.md"
         data-doxygen="md_PROJECT.html">
  <a href="../PROJECT.md">Project</a>
</span>
 ·
⭐ <span class="md-link"
         data-github="FEATURE.md"
         data-doxygen="md_Version_FEATURE.html">
  <a href="FEATURE.md">Features</a>
</span>
 ·
🎮 <span class="md-link"
         data-github="../Usage/USECASES.md"
         data-doxygen="md_Usage_USECASES.html">
  <a href="../Usage/USECASES.md">Use Cases</a>
</span>
 ·
🏷️ <span class="md-link"
         data-github="VERSION.md"
         data-doxygen="md_Version_VERSION.html">
  <a href="VERSION.md">Versions</a>
</span>
 ·
📜 <span class="md-link"
         data-github="RELEASE_POLICY.md"
         data-doxygen="md_Version_RELEASE_POLICY.html">
  <a href="RELEASE_POLICY.md">Release Policy</a>
</span>
 ·
📦 <span class="md-link"
         data-github="NAMESPACE.md"
         data-doxygen="md_Version_NAMESPACE.html">
  <a href="NAMESPACE.md">Namespaces</a>
</span>
 ·
🧩 <span class="md-link"
         data-github="API.md"
         data-doxygen="md_Version_API.html">
  <a href="API.md">APIs</a>
</span>
 ·
🐞 <span class="md-link"
         data-github="BUG.md"
         data-doxygen="md_Version_BUG.html">
  <a href="BUG.md">Bugs</a>
</span>
 ·
🔧 <span class="md-link"
         data-github="FIX.md"
         data-doxygen="md_Version_FIX.html">
  <a href="FIX.md">Fixes</a>
</span>
 ·
📋 <span class="md-link"
         data-github="CHANGELOG.md"
         data-doxygen="md_Version_CHANGELOG.html">
  <a href="CHANGELOG.md">Change Log</a>
</span>
 ·
☎️ <span class="md-link"
         data-github="../CONTACT_US.md"
         data-doxygen="md_CONTACT_US.html">
  <a href="../CONTACT_US.md">Contact Us</a>
</span>

<br>

<p>

This page provides an **example of API Reference** for the <b>README Template</b>. The APIs listed here are **fictitious** and serve as a placeholder to demonstrate the structure.  
In a real project, this section is fully customizable and can be updated by the project maintainer to reflect the actual APIs, parameters, namespaces, versions, and roles.

</p>

<br>
<br>

<!-- Table of Contents -->

<a name="table-of-contents"></a>

### 📓 Table of Contents

Navigation index to fast explore the content:

- [API Characteristics](#characteristics)
- [API Reference](#api-reference)
- [How To](#how-to)
  - [How To Integrate APIs](#how-to-integrate-apis)
  - [How To Develop APIs](#how-to-develop-apis)
- [FAQ](#faq)
- [Contact us](#contact-us)
- [See Also](#see-also)
- [Official Links](#official-links)

<br>
<br>

<a id="characteristics"></a>

# Characteristics

Each API defines:
  - a set of <em>Parameters</em> to specify during the <b>API Request</b>.
  - a <em>Response Type</em> returned on <b>API Response</b>. Both depend on the given API <b>implementation specifications</b> so read the single <b>API documentation</b> to know how each API act and how to use it.

<br>

## 🎮 Used by
APIs are used by:
- <em>Features</em> to implement themself. Each API declare into which features they are used.
- <em>Actors</em> into <em>Use Cases</em> to perform tasks. Each API declare for which actors they are suited for.

## ⭐ Versions
Each API is available on a specific <em>Version</em> and can contain <em>Bugs</em> solved as soon as possible by <em>Fixes</em>. Each API release follows the 
<span class="md-link" data-github="RELEASE_POLICY.md" data-doxygen="md_Version_RELEASE_POLICY.html">
  <a href="RELEASE_POLICY.md"><b>Release Policy</b></a>
</span>
and declares the implemented versions, the discovered bugs, and provided fixes.

## 🧩 Collection
APIs are collected into <em>Namespaces</em> that expose the API and other related resources to use the API properly. Each API declares the <em>Namespace</em> that contains it.

## 🔐 Accessibility
API's accessibility is <em>Role</em> based. If the role used by the actor to access the API does not correspond to the admitted, the API will fail and return a permission fail response. Each API declares the admitted roles.

## ↩️ Changes
An <em>API</em> can be modified by some <em>Changes</em> during the <b>Readme Template</b> lifecycle, so read the 
<span class="md-link" data-github="CHANGELOG.md" data-doxygen="md_Version_CHANGELOG.html">
  <a href="CHANGELOG.md"><b>Change Log</b></a>
</span>
to be updated with the latest API changes.

## 🛠️ Extendability
It is possible to extend the set of APIs of each namespace by adding new APIs. To know how, follow the 
<span class="md-link" data-github="DEVELOPMENT_GUIDE.md" data-doxygen="md_Usage_DEVELOPMENT_GUIDE.html">
  <a href="DEVELOPMENT_GUIDE.md"><b>Development Guide</b></a>
</span>.

  

<br>

<!-- API Reference -->

<a id="api-reference"></a>

# API Reference

<br>

The whole set of API is divided into <b>Namespaces</b>. Each namespace is composed by some <b>Sub-Namespaces</b> that specialize it. The following navigation index contains all APIs grouped by namespaces:

- [Control](#control)
  - [Command](#command)
    - int <a href="#start">Start</a> (bool fast_start, bool exit_on_fail, int *level) - Initialize and start the control subsystem.<br>
    - int <a href="#exit">Exit</a> (bool fast_exit, bool exit_on_fail, int *level) - Safely terminate the control subsystem.<br> 
  - [Process](#process)
    - int <a href="#terminate">Terminate</a>() - Terminate the currently running process or subsystem.<br>
    - <a href="#wait">Wait</a>() - Wait for the completion of the process or child task.<br>

<br>
<br>

<a name="control"></a>

# Control


The <code>Control</code> namespace provides control capabilities and resources with its sub-namespace system:

- [Command](#command)
    - int <a href="#start">Start</a>(bool fast_start, bool exit_on_fail, int *level> - Initialize and start the control subsystem.<br>
    - int <a href="#exit">Exit</a>(bool fast_exit, bool exit_on_fail, int *level) - Safely terminate the control subsystem.<br> 
- [Process](#process)
    - int <a href="#terminate">Terminate</a>() - Terminate the currently running process or subsystem.<br>
    - <a href="#wait">Wait</a>() - Wait for the completion of the process or child task.<br>

<br>


<a name="command"></a>

## Command

The <code>Command</code> sub-namespace provides process and subsystem control operations.

  <summary><b>Command</b> Namespace</summary>
  <p>The <b>Command</b> namespace includes initialization and termination APIs.</p>

 - [Command](#command)
    - int <a href="#start">Start</a>(bool fast_start, bool exit_on_fail, int *level> - Initialize and start the control subsystem.<br>
    - int <a href="#exit">Exit</a>(bool fast_exit, bool exit_on_fail, int *level) - Safely terminate the control subsystem.<br> 

<br>
<br>

<br>
<br>

<!-- Start -->

<a name="start"></a>

### Start 📎

<br>


```html
int Start(bool fast_start, bool exit_on_fail, int level*);

```

<br>


##### 🧩 NAMESPACE


<span class="md-link" data-github="NAMESPACE.md#command" data-doxygen="md_Version_NAMESPACE.html#command">
  <a href="NAMESPACE.md#command">Control::Command</a>
</span>

<br>


##### FULL-DESCRIPTOR

Control::Command::Start
<br>

##### 📋 DESCRIPTION

Start is a control command that starts 
<br>

##### ⚠️ REQUIREMENTS

Start requires v1.0.0 or above
<br>

##### AVAILABLE FROM

version > v1.0.0
<br>

##### 🛠️ PARAMETERS
 
- **bool fast_start**: enable fast start on start operation 
- **bool exit_on_fail**: exit when a fail during start occurs
- **int level***: optional level integer used to start 
<br>

##### ↩️ RETURNS

- **int result**:
<br>

##### ⛔ EXCEPTIONS

- **ResourceNotFoundException**: This exception occurs when the resources to start are not available.
- **PermissionDeinedException**: This exception occurs when permissions to start are not granted.
<br>

##### ❌ ERRORS
<br>

##### ⭐ EXAMPLES
<br>

##### 📋 NOTES

> When using start, be sure to import Control::Command namespace

<br>
<br>

<a name="exit"></a>


<!-- Exit -->
### Exit 📎
<br>


```html

int Exit(bool fast_exit, bool exit_on_fail, int level*);

```

<br>

##### 🧩 NAMESPACE

<span class="md-link" data-github="NAMESPACE.md#command" data-doxygen="md_Version_NAMESPACE.html#command">
  <a href="NAMESPACE.md#command">Control::Command</a>
</span>

<br>

##### FULL-DESCRIPTOR

Control::Command::Exit
<br>

##### 📋 DESCRIPTION

Exit is a control command that exites 
<br>

##### ⚠️ REQUIREMENTS

Exit requires v1.0.0 or above
<br>

##### AVAILABLE FROM

version > v1.0.0
<br>

##### PARAMETERS
 
- **bool fast_exit**: enable fast exit on exit operation 
- **bool exit_on_fail**: exit when a fail during exit occurs
- **int level***: optional level integer used to exit 
<br>

##### ↩️ RETURNS

- **int result** 
<br>

##### ⛔  EXCEPTIONS

- **ResourceNotFoundException**: This exception occurs when the resources to start are not available.
- **PermissionDeinedException**: This exception occurs when permissions to start are not granted.
<br>

##### ❌ ERRORS 
<br>

##### ⭐ EXAMPLES
<br>

##### 📋 NOTES

> When using exit, be sure to import Control::Command namespace

<br>
<br>

<a name="process"></a>

## Process

  <summary><b>Process</b> Namespace</summary>
  <p>The <b>Process</b> subnamespace provides process handling APIs.</p>

  - [Process](#process)
    - int <a href="#terminate">Terminate</a>() - Terminate the currently running process or subsystem.<br>
    - <a href="#wait">Wait</a>() - Wait for the completion of the process or child task.<br>


<br>
<br>

<!-- Terminate -->

<a name="terminate"></a>


### Terminate 📎
<br>

```html

int Terminate();

```

<br>

##### 🧩 NAMESPACE

<span class="md-link" data-github="NAMESPACE.md#process" data-doxygen="md_Version_NAMESPACE.html#process">
  <a href="NAMESPACE.md#process">Control::Process</a>
</span>


<br>

##### FULL-DESCRIPTOR

Control::Process::Exit
<br>

##### 📋 DESCRIPTION

Terminate is a control command that exites 
<br>

##### ⚠️ REQUIREMENTS

Terminate requires v1.0.0 or above
<br>

##### AVAILABLE FROM

version > v1.0.0
<br>

##### ↩️ RETURNS 

- **int result** 
<br>

##### ⛔  EXCEPTIONS
 
- **PermissionDeinedException**
<br>

##### ❌ ERRORS 

<br>

##### EXAMPLES

##### 📋 NOTES

> When using terminate, be sure to import Control::Process namespace

<br>
<br>


<a name="wait"></a>

<!-- Wait -->

### Wait 📎
<br>

```html
  int Wait();
```
<br>

##### 🧩 NAMESPACE

<a class="md-link" data-github="Version/NAMESPACE.md#process" data-doxygen="md_Version_NAMESPACE.html#process">Control::Process</a>

<br>

##### FULL-DESCRIPTOR


Control::Process::Wait
<br>

##### 📋 DESCRIPTION

Wait is a control command that waites 
<br>

##### ⚠️ REQUIREMENTS

Wait requires v1.0.0 or above
<br>

##### AVAILABLE FROM

version > v1.0.0
<br>

##### ↩️ RETURNS
 
- **int result** 
<br>

##### ⛔  EXCEPTIONS

- **PermissionDeinedException**:
<br>

##### ❌ ERRORS
<br>

##### ⭐ EXAMPLES
<br>

##### 📋 NOTES

> When using wait, be sure to import Control::Process namespace

<br>
<br>

<a name="how-to"></a>

# How To 🛠️

[Table of Contents](#table-of-contents)

In this section we explain **How To** perform certain tasks involving APIs:

- <a href="#how-to-integrate-apis">How To Integrate APIs</a> – helps a Developer integrate <b>Readme Template</b> APIs into new products.
- <a href="#how-to-develop-apis">How To Develop APIs</a> – helps a Developer create new <b>Readme Template</b> APIs.

<br>

<a name="how-to-integrate-apis"></a>

### How To Integrate APIs

[Table of Contents](#table-of-contents)

<br>

<a name="how-to-develop-apis"></a>

### How To Develop APIs

[Table of Contents](#table-of-contents)

<br><br>

<a name="see-also"></a>

# See Also

[Table of Contents](#table-of-contents)

The following documents are related:

<ul>
  <li>
    <span class="md-link" data-github="Version/RELEASE_POLICY.md" data-doxygen="md_Version_RELEASE_POLICY.html">
      <a href="RELEASE_POLICY.md"><b>Release Policy</b></a>
    </span> file, named <code>RELEASE_POLICY.md</code>, contains the <b>Release Policy</b> standard adopted in <b>README Template</b>.
  </li>
  <li>
    <span class="md-link" data-github="Version/FEATURE.md" data-doxygen="md_Version_FEATURE.html">
      <a href="FEATURE.md"><b>Features</b></a>
    </span> file, named <code>FEATURE.md</code>, contains the <b>Features</b> of <b>README Template</b>.
  </li>
  <li>
    <span class="md-link" data-github="Version/API.md" data-doxygen="md_Version_API.html">
      <a href="API.md"><b>APIs</b></a>
    </span> file, named <code>API.md</code>, contains the <b>APIs</b> of <b>README Template</b>.
  </li>
  <li>
    <span class="md-link" data-github="Version/CHANGELOG.md" data-doxygen="md_Version_CHANGELOG.html">
      <a href="CHANGELOG.md"><b>Change Log</b></a>
    </span> file, named <code>CHANGELOG.md</code>, contains the <b>Changes</b> made in <b>README Template</b>.
  </li>
  <li>
    <span class="md-link" data-github="Version/NAMESPACE.md" data-doxygen="md_Version_NAMESPACE.html">
      <a href="NAMESPACE.md"><b>Namespaces</b></a>
    </span> file, named <code>NAMESPACE.md</code>, contains the <b>Namespace</b> architecture of <b>README Template</b>.
  </li>
  <li>
    <span class="md-link" data-github="Version/BUG.md" data-doxygen="md_Version_BUG.html">
      <a href="BUG.md"><b>Bugs</b></a>
    </span> file, named <code>BUG.md</code>, contains the <b>Bugs</b> identified in <b>README Template</b>.
  </li>
  <li>
    <span class="md-link" data-github="Version/FIX.md" data-doxygen="md_Version_FIX.html">
      <a href="FIX.md"><b>Fixes</b></a>
    </span> file, named <code>FIX.md</code>, contains the <b>Fixes</b> applied to <b>README Template</b>.
  </li>
</ul>

<br>
<br>

<a name="faq"></a>

# FAQ ❓

Here you can find the Frequently Asked Questions and Answers.

<br><br>

<a name="contact-us"></a>

# Contact us ☎️

For **more information** on <b>Readme Template</b> 
<span class="md-link" data-github="CONTACT_US.md" data-doxygen="md_CONTACT_US.html">
  <a href="../CONTACT_US.md"><b>contact us</b></a>
</span>.

<br>
<br>

<a name="official-links"></a>

# Official Links

[Table of Contents](#table-of-contents)

* [SemVer](https://www.semver.org) – complete guide to **Semantic Versioning**. 
* [Doxygen](https://www.doxygen.nl/index.html) – documentation generator for source code.
* [GitHub](https://github.com) – hosting and collaboration platform for Git repositories.
* [Git](https://git-scm.com) – version control system for source code.
* [GNU Make](https://www.gnu.org/software/make/) – build automation tool to compile projects.

<br><br>

