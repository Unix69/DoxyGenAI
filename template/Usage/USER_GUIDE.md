<div align="left">

  <h1> 👤 User Guide </h1>
  
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
    This **User Guide** provides a complete overview of how to use **<b>Readme Template</b>**, perform common operations, and take advantage of the available features.
  </p>

</div>

<br><br>

<a name="table-of-contents"></a>

### 📓 Table of Contents
- [User Overview](#user-overview)
- [User Operations](#user-operations)
- [How To](#how-to)
- [Other Guides](#other-guides)
- [FAQ](#faq)
- [Contacts](#contact-us)

<br>
<br>

<a name="user-overview"></a>

# User Overview 👤

[Table of Contents](#table-of-contents)

This section explains the **main interactions for end-users** of the README Template. Users can explore the template structure, navigate Markdown documentation, and understand how documentation integrates with Doxygen-generated HTML.

Key points:

- The template provides a **standardized layout** for documenting projects.
- Markdown files are **modular**, representing features, versions, API, namespaces, bugs, fixes, and guides.
- Users can quickly navigate **User Guide**, **Admin Guide**, and **Developer Guide** using the Doxygen HTML interface.

<br><br>

# User Operations 🧭

[Table of Contents](#table-of-contents)

Operations that a user can perform with the README Template:

1. Explore the **directory structure** to understand where each type of documentation is located (`Version/`, `Usage/` folders).
2. Open Markdown files in a text editor to read or modify content.
3. Use the **Makefile** to generate the Doxygen HTML documentation (<code>make build</code> → <code>make doc</code>).
4. Navigate the **interactive HTML site** to explore links between Markdown files and source code.
5. Track **features, API endpoints, versions, bugs, and fixes** directly in the HTML interface.
6. Access **contact and project information** for collaboration.

<br><br>

# How To 🛠️

[Table of Contents](#table-of-contents)

Step-by-step instructions to use the README Template effectively:

<a name="how-to-start"></a>

## How to start the documentation process

1. Clone the repository:  
   <code>git clone https://github.com/Unix69/EmbeddedDocsTemplates.git</code>
2. Navigate into the project folder:  
   <code>cd EmbeddedDocsTemplates</code>
3. Open Markdown files under `./Usage` or `./Version` to explore content.
4. Run the Makefile to generate documentation:  
   <code>make build</code>  
   <code>make doc</code>
5. Open the generated HTML in `docs/html/index.html` to browse the interactive documentation.

<br>
<br>

<a name="how-to-use-feature"></a>

## How to use a feature

1. Select the Markdown file representing the feature or section (e.g., `FEATURE.md`).
2. Edit or add documentation, including Doxygen tags like `@feature`, `@api`, or `@namespace`.
3. Rebuild the documentation using <code>make doc</code>.
4. Verify that updates are reflected in the HTML site with correct linking to source code and other Markdown files.

<br><br>

# Other Guides 📚

| Role | Reference | Description |
|------|------------|-------------|
| 🧑‍💼 **Admin Guide** | <span class="md-link" data-github="Usage/ADMINISTRATOR_GUIDE.md" data-doxygen="md_Usage_ADMINISTRATOR_GUIDE.html"><a href="ADMINISTRATOR_GUIDE.md"><b>ADMINISTRATOR_GUIDE.md</b></a></span> | Configuration, maintenance, and management of the template |
| 🧑‍💻 **Developer Guide** | <span class="md-link" data-github="Usage/DEVELOPMENT_GUIDE.md" data-doxygen="md_Usage_DEVELOPMENT_GUIDE.html"><a href="DEVELOPMENT_GUIDE.md"><b>DEVELOPMENT_GUIDE.md</b></a></span> | Guidelines for extending or integrating the template in projects |

<br>
<br>

# FAQ ❓

- **Q:** How do I add a new section to the template?  
  **A:** Create a new Markdown file under `Usage/` or `Version/`, then add it to the table of contents.

- **Q:** How can I regenerate the HTML after changes?  
  **A:** Run <code>make doc</code> to rebuild the site. All Markdown changes will appear in the HTML.

- **Q:** Can I customize the HTML layout?  
  **A:** Yes, edit `header.html`, `footer.html`, or `stylesheet.css` for visual customization.

<br>
<br>

# Contact Us ☎️

For more information about the README Template → <span class="md-link" data-github="CONTACT_US.md" data-doxygen="md_CONTACT_US.html"><a href="CONTACT_US.md"><b>Contact Page</b></a></span>

<br><br>
</div>

