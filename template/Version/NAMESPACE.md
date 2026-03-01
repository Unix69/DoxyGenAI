<h1>
  📦 Namespace
</h1>

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
         data-github="PROJECT.md"
         data-doxygen="md_PROJECT.html">
  <a href="../PROJECT.md">Project</a>
</span>
 ·
⭐ <span class="md-link"
         data-github="Version/FEATURE.md"
         data-doxygen="md_Version_FEATURE.html">
  <a href="FEATURE.md">Features</a>
</span>
 ·
🎮 <span class="md-link"
         data-github="Usage/USECASES.md"
         data-doxygen="md_Usage_USECASES.html">
  <a href="../Usage/USECASES.md">Use Cases</a>
</span>
 ·
🏷️ <span class="md-link"
         data-github="Version/VERSION.md"
         data-doxygen="md_Version_VERSION.html">
  <a href="VERSION.md">Versions</a>
</span>
 ·
📜 <span class="md-link"
         data-github="Version/RELEASE_POLICY.md"
         data-doxygen="md_Version_RELEASE_POLICY.html">
  <a href="RELEASE_POLICY.md">Release Policy</a>
</span>
 ·
📦 <span class="md-link"
         data-github="Version/NAMESPACE.md"
         data-doxygen="md_Version_NAMESPACE.html">
  <a href="NAMESPACE.md">Namespaces</a>
</span>
 ·
🧩 <span class="md-link"
         data-github="Version/API.md"
         data-doxygen="md_Version_API.html">
  <a href="API.md">APIs</a>
</span>
 ·
🐞 <span class="md-link"
         data-github="Version/BUG.md"
         data-doxygen="md_Version_BUG.html">
  <a href="BUG.md">Bugs</a>
</span>
 ·
🔧 <span class="md-link"
         data-github="Version/FIX.md"
         data-doxygen="md_Version_FIX.html">
  <a href="FIX.md">Fixes</a>
</span>
 ·
📋 <span class="md-link"
         data-github="Version/CHANGELOG.md"
         data-doxygen="md_Version_CHANGELOG.html">
  <a href="CHANGELOG.md">Change Log</a>
</span>
 ·
☎️ <span class="md-link"
         data-github="CONTACT_US.md"
         data-doxygen="md_CONTACT_US.html">
  <a href="../CONTACT_US.md">Contact Us</a>
</span>

<br>


This page provides an **example of Namespace Reference** for the <b>README Template</b>. The Namespaces listed here are **fictitious** and serve as a placeholder to demonstrate the structure.  
In a real project, this section is fully customizable and can be updated by the project maintainer to reflect the actual Namespaces, parameters, namespaces, versions, and roles.


<br>

<a name="table-of-contents"></a>
### 📓 Table of Contents

- [Namespace Reference](#namespace-reference)
- [How To](#how-to)
  - [How To Import Namespaces](#how-to-import-namespaces)
  - [How To Address APIs through Namespaces](#how-to-address-apis-through-namespaces)
- [See Also](#see-also)
- [FAQ](#faq)
- [Official Links](#official-links)

<br><br>

<a name="namespace-reference"></a>

## Namespace Reference

The following navigation index represents the <b>Readme Template</b> namespace division into namespaces and sub-namespaces:

- [Control](#control)
  - [Command](#command)
  - [Process](#process)

<br><br><br>

<a name="control"></a>
## 📎 Control

*Control* is a **Namespace** of <b>Readme Template</b> **containing all control namespaces and APIs used to manage <b>Readme Template</b>**

**Requirements**:
- ⚠️ Minimum required version: *v1.0.0*

**State**:
- **Obsolete** from version *v1.0.0*
- **Deprecated** from version *v2.0.0* :x:

| 📦 Sub Namespace | Full Name | Brief Description |
| ---------------- | --------- | ---------------- |
| <a href="#command">Command</a> | *Control::Command* | Brief Description |
| <a href="#process">Process</a> | *Control::Process* | Brief Description |

| 🔧 Attribute | Full Name | Type | Description |
| ------------ | --------- | ---- | ----------- |
| ***fast_start*** | *Control::fast_start* | **bool** | enable fast start on start operation |
| ***exit_on_fail*** | *Control::exit_on_fail* | **bool** | exit when a fail during start occurs |
| ***level*** | *Control::level* | **int** | optional level integer used to start |

| ⭐ Property | Full Name | Type | Permissions | Description |
| ----------- | --------- | ---- | ----------- | ----------- |
| ***fast_start*** | *Control::fast_start* | **bool** | RW | enable fast start on start operation |
| ***exit_on_fail*** | *Control::exit_on_fail* | **bool** | RW | exit when a fail during start occurs |
| ***level*** | *Control::level* | **int** | R | optional level integer used to start |

*Control* namespace contains the following API:

| 🧩 API | Full Name | Brief Description |
| --- | --------- | ---------------- |
| ***<a class="md-link" data-github="Version/API.md#start" data-doxygen="md_Version_API.html#start" href="API.md#start">start</a>*** | *control::command::start* | permits to initialize and start the control process |
| ***<a class="md-link" data-github="Version/API.md#exit" data-doxygen="md_Version_API.html#exit" href="API.md#exit">exit</a>*** | *control::command::exit* | permits to terminate the control process subsystem |
| ***<a class="md-link" data-github="Version/API.md#terminate" data-doxygen="md_Version_API.html#terminate" href="API.md#terminate">terminate</a>*** | *control::process::terminate* | safely terminate the control process subsystem |
| ***<a class="md-link" data-github="Version/API.md#wait" data-doxygen="md_Version_API.html#wait" href="API.md#wait">wait</a>*** | *control::process::wait* | wait for completion of control process or child task |

<br><br>

<a name="command"></a>
## 📎 Command

*Command* is a **Sub-Namespace** of <a href="#control">Control</a> **containing all command APIs used to execute commands on <b>Readme Template</b>**

**Dependencies**:
- <a href="#control">Control</a>

**Requirements**:
- ⚠️ Minimum required version: *v1.0.0*

**State**:
- **Obsolete** from version *v1.0.0*
- **Deprecated** from version *v2.0.0* :x:

| 🔧 Attribute | Full Name | Type | Description |
| ------------ | --------- | ---- | ----------- |
| ***fast_start*** | *Control::Command::fast_start* | **bool** | enable fast start on start operation |
| ***exit_on_fail*** | *Control::Command::exit_on_fail* | **bool** | exit when a fail during start occurs |
| ***level*** | *Control::Command::level* | **int** | optional level integer used to start |

| ⭐ Property | Full Name | Type | Permissions | Description |
| ----------- | --------- | ---- | ----------- | ----------- |
| ***fast_start*** | *Control::Command::fast_start* | **bool** | RW | enable fast start on start operation |
| ***exit_on_fail*** | *Control::Command::exit_on_fail* | **bool** | RW | exit when a fail during start occurs |
| ***level*** | *Control::Command::level* | **int** | R | optional level integer used to start |

*Command* sub-namespace contains the following API:

| 🧩 API | Full Name | Brief Description |
| --- | --------- | ---------------- |
| ***<a class="md-link" data-github="Version/API.md#start" data-doxygen="md_Version_API.html#start" href="API.md#start">start</a>*** | *control::command::start* | permits to initialize and start the control process |
| ***<a class="md-link" data-github="Version/API.md#exit" data-doxygen="md_Version_API.html#exit" href="API.md#exit">exit</a>*** | *control::command::exit* | permits to terminate the control process subsystem |

<br><br>

<a name="process"></a>
## 📎 Process

*Process* is a **Sub-Namespace** of <a href="#control">Control</a> **containing all process APIs used to manage processes in <b>Readme Template</b>**

**Dependencies**:
- <a href="#control">Control</a>

**Requirements**:
- ⚠️ Minimum required version: *v1.0.0*

**State**:
- **Obsolete** from version *v1.0.0*
- **Deprecated** from version *v2.0.0* :x:

| 🔧 Attribute | Full Name | Type | Description |
| ------------ | --------- | ---- | ----------- |
| ***fast_start*** | *Control::Process::fast_start* | **bool** | enable fast start on start operation |
| ***exit_on_fail*** | *Control::Process::exit_on_fail* | **bool** | exit when a fail during start occurs |
| ***level*** | *Control::Process::level* | **int** | optional level integer used to start |

| ⭐ Property | Full Name | Type | Permissions | Description |
| ----------- | --------- | ---- | ----------- | ----------- |
| ***fast_start*** | *Control::Process::fast_start* | **bool** | RW | enable fast start on start operation |
| ***exit_on_fail*** | *Control::Process::exit_on_fail* | **bool** | RW | exit when a fail during start occurs |
| ***level*** | *Control::Process::level* | **int** | R | optional level integer used to start |

*Process* sub-namespace contains the following API:

| 🧩 API | Full Name | Brief Description |
| --- | --------- | ---------------- |
| ***<a class="md-link" data-github="Version/API.md#terminate" data-doxygen="md_Version_API.html#terminate" href="API.md#terminate">terminate</a>*** | *control::process::terminate* | safely terminate the control process subsystem |
| ***<a class="md-link" data-github="Version/API.md#wait" data-doxygen="md_Version_API.html#wait" href="API.md#wait">wait</a>*** | *control::process::wait* | wait for completion of the control process or child task |

<br><br>

<a name="how-to"></a>
# How To

- [How To Import ⬇️ Namespaces](#how-to-import-namespaces)
- [How To Address APIs 🧩 through Namespaces](#how-to-address-apis-through-namespaces)

<br>

<a name="how-to-import-namespaces"></a>
### ⬇️ How To Import Namespaces

- Explains how a **Developer** can import <b>Readme Template</b> namespaces into new projects.

<br>

<a name="how-to-address-apis-through-namespaces"></a>
### 🧩 How To Address APIs through Namespaces

- Explains how a **Developer** can address APIs via their namespaces.

<br><br>

<a name="see-also"></a>

# See Also

[Table of Contents](#table-of-contents)

<br>

The following documents are related to this:

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

<br>
<br>

<a name="contact-us"></a>

# Contact us ☎️

For **more information** on <b>Readme Template</b> 
<span class="md-link"
      data-github="CONTACT_US.md"
      data-doxygen="md_CONTACT_US.html">
  <a href="../CONTACT_US.md"><b>contact us</b></a>
</span>.

<a name="official-links"></a>

<!-- Official Links -->

# Official Links

[Table of Contents](#table-of-contents)

* [SemVer](https://www.semver.org) – A complete guide to **Semantic Versioning**. 
* [Doxygen](https://www.doxygen.nl/index.html) – **Documentation generator** for source code.
* [GitHub](https://github.com) – **Hosting** and **collaboration platform** for **Git** repositories.
* [Git](https://git-scm.com) – **Version control** system to manage source code.
* [GNU Make](https://www.gnu.org/software/make/) – **Build automation tool** to compile projects.

<br>
<br>
