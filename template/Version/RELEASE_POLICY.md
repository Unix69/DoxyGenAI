<h1>
    📜 Release Policy 
</h1>

  <!-- Badges -->
  <p>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/graphs/contributors"><img src="https://img.shields.io/github/contributors/Unix69/EmbeddedDocsTemplates" alt="contributors" /></a>
    <a href=""><img src="https://img.shields.io/github/last-commit/Unix69/EmbeddedDocsTemplates" alt="last update" /></a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/network/members"><img src="https://img.shields.io/github/forks/Unix69/EmbeddedDocsTemplates" alt="forks" /></a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/stargazers"><img src="https://img.shields.io/github/stars/Unix69/EmbeddedDocsTemplates" alt="stars"/></a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/issues/"><img src="https://img.shields.io/github/issues/Unix69/EmbeddedDocsTemplates" alt="open issues" /></a>
    <a href="https://github.com/Unix69/EmbeddedDocsTemplates/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Unix69/EmbeddedDocsTemplates.svg" alt="license" /></a>
  </p>
  
<br>

<p>
	The **Release Policy** specifies and explains the versioning protocol followed for **[PROJECT-NAME]**.
	Knowing the **Release Policy**, helps to characterize a given release version and its temporarly evolution.
	So **reading the Release Policy is a best practice** when you are approaching to **[PROJECT-NAME]**.
</p>


<br/>



<!-- Table of Contents -->

<a name="table-of-contents"></a>

### 📓 Table of Contents

Navigation index to fast explore the content:

- [Release Policy Standard](#release-policy-standard)
- [Version Label Encoding](#version-label-encoding)
- [Versioning Rules](#versioning-rules)	
	* [Versioning Precedence Rules](#versioning-precedence-rules)
	* [Versioning Grammar Rules](#versioning-grammar-rules)
- [Contact us](#contact-us)
- [FAQ](#faq)
- [See Also](#see-also)
- [Official Links](#official-links)


<br>
<br>

<!-- Release Policy Standard -->

# Release Policy Standard

[Table of Contents](#table-of-contents)

**[PROJECT-NAME]** follows *Semantic Versioning (SemVer)* whereby the *Version Identifier (VID)* expresses a meaning about the characteristics of the identified software release, by encoding them into some ordered *Labels* where each of them specify
a software release state feature.

SemVer is applicable from **[PROJECT-NAME] v1.0.0** onwards.

SemVer defines a software version given its *APIs*, *Features*, *Bugs* and *Fixes*. A new software version contains *API*, *Features*, *Bug* or *Fix* changes respect to the lower version. The version changes even in case of 
pre-release or build data specification, but this changes do not imply any *API*, *Features* or *Bugs* level changes. However *API* level changes defines **MAJOR** version upgrades, *Feature* level changes define **MINOR** version upgrades and
*Bugs* level changes define **PATCH** version upgrades

SemVer's VIDs are essentially composed by a mandatory part, called **MAIN-VID**, and an optional part named **EXT-VID** in this format [NORM-VID][EXT-VID].

| SUB VID   | Description                                                                                                                                                                                   | Format |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| MAIN-VID  | **Static** structured and **Mandatory** identifier expressed by dot separated **MAJOR-VID**, **MINOR-VID** and **PATCH-VID** labels  | <ul><li> [MAJOR-VID].[MINOR-VID].[PATCH-VID] </li></ul> |
| EXT-VID   | **Dynamic** structured and **Optional** identifier expressed by **-/+** separated **PRE-RELEASE-VID**, **BUILD-METADATA-VID** labels | <ul><li> [MAIN-VID]-[PRE-RELEASE-VID]+[BUILD-METADATA-VID]</li><li>[MAIN-VID]-[PRE-RELEASE-VID]</li><li>[MAIN-VID]+[BUILD-METADATA-VID]</li></ul> |

So the **fully detailed VID** is encoded by the following expression:

<ul><li>[MAJOR-VID].[MINOR-VID].[PATCH-VID][-PRE-RELEASE-VID][+BUILD-METADATA-VID]</ul></li>

<br>

> 📋 **Notes**: each of **EXT-VID's** labels can be used optionally

<br>
<br>

<!-- Version Label Encoding -->

# Version Label Encoding 

[Table of Contents](#table-of-contents)

<br>

<img src="Images/semver.png" alt="SemVer" style="align: center;"> 

<br>

This project identifes the first part of the verion identifier as the MAIN-VID and the second part as external version identifier EXT-VID

| MAIN-VID Labels | Description                                                                                         | Encoding                                                                | Hints |
| --------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MAJOR-VID       | It defines the major version identifier and it identifies **incompatible API changes**              | **Non negative integer** increased numerically. It **cannot be empty**. | <ul><li> 0 identify the initial development version. Anything can change at any time. The public API are not considered stable</li><li>It is incremented if any backward incompatible changes are introduced to the public API. </li><li> It can also include minor and patch level changes </li><li> **PATCH-VID** and **MINOR-VID** are resetted to 0 when major version is incremented</li></ul> |
| MINOR-VID       | It defines the minor version identifier and it identifies **backward compatible feature additions** | **Non negative integer** increased numerically. It **cannot be empty**. | <ul><li> It is incremented if new, backward compatible functionality is introduced to the public API </li><li> It is incremented if any public API functionality is marked as deprecated </li><li> It is incremented if substantial new functionality or improvements are introduced within the private code. It can include patch level changes </li></ul> |
| PATCH-VID       | It defines the patch version identifier and it identifies **backward compatible bug fixes**         | **Non negative integer** increased numerically. It **cannot be empty**. | <ul><li> It is incremented if only backward compatible bug fixes are introduced. </li><li> A bug fix is defined as an internal change that fixes incorrect behavior </li></ul> |

<br>

| EXT-VID Labels     | Description                                                                                                                                                                                                   | Encoding                                                                                                                                                                                                        | Hints                                                                                             	                                                                                                                                                                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | 
| PRE-RELEASE-VID    | It defines the pre-release version identifier and it identify an **unstable software version** that **might not satisfy the intended compatibility requirements** as denoted by its associated **[MAIN-VID]** | It is precedeed by an Hyphen (**-**) and a series of dot separated identifiers, immediately following the **PATCH-VID**. Each identifier comprise **only ASCII alphanumerics and hyphens** and **cannot be empty**.                        | <ul><li> Numeric identifiers do not include leading zeroes </li><li> Pre-release versions have a lower precedence than the associated normal version </li><li> A pre-release version indicates that the version is unstable and might not satisfy the intended compatibility requirements as denoted by its associated normal version </li></ul> |
| BUILD-METADATA-VID | It defines the **metadata used into building process**                                                                                                                                                        | It is precedeed by a Plus (**+**) sign and a series of dot separated identifiers, immediately following the **PRE-RELEASE-VID** or **PATCH-VID**. Each identifier comprise **only ASCII alphanumerics and hyphens** and **cannot be empty**. | <ul><li> Build metadata has to be ignored when determining version precedence </li><li> Thus two versions that differ only in the build metadata, have the same precedence </li></ul>                                                                                                                                                            |

<br>

> :memo: **Notes** <ul><li> Once a Software version has been released, the contents of that version will be not modified anymore. Any modifications are released as a new version </li><li> **1.0.0** defines the public API. The way in which the version number is incremented after this release is dependent on this public API and how it changes </li></ul>

<br>

<!-- Versioning Rules -->

# Versioning Rules 📘

[Table of Contents](#table-of-contents)

This section contains version grammar and version precedence rules in order to validate a **VID** or compare two **VIDs** each other. Following this basic rules is helpful to understand <a href="https://www.semver.org" target="_blank">SemVer</a> and to move between different software releases.

<br>
<br>

<!-- Versioning Precedence Rules -->

## Versioning Precedence Rules

[Table of Contents](#table-of-contents)

Precedence refers to how **VIDs** are compared to each other when ordered. The following precedence rules can be used to determine the precedence of a given **[MAIN-VID]** or **[EXT-VID]** respect to another:

- Precedence are calculated by **separating the version into major, minor, patch and pre-release identifiers** in that order (build metadata does not figure into precedence).
- **Precedence is determined by the first difference when comparing each of these identifiers from left to right** as follows: major, minor, and patch versions are always compared numerically.
	+ Example: **1.0.0** < **2.0.0** < **2.1.0** < **2.1.1**.
- When **major, minor, and patch are equal**, a **pre-release version has lower precedence than a normal version**:
	+ Example: **1.0.0-alpha** < **1.0.0**.
- Precedence for two pre-release versions with the same major, minor, and patch version are determined by comparing each dot separated identifier from left to right until a difference is found as follows:
	+ **Identifiers consisting of only digits are compared numerically**.
	+ **Identifiers with letters or hyphens are compared lexically in ASCII sort order**.
	+ **Numeric identifiers always have lower precedence than non-numeric identifiers**.
	+ A **larger set of pre-release fields has a higher precedence than a smaller set**, if all of the preceding identifiers are equal.
		+ Example: **1.0.0-alpha** < **1.0.0-alpha.1** < **1.0.0-alpha.beta** < **1.0.0-beta** < **1.0.0-beta.2** < **1.0.0-beta.11** < **1.0.0-rc.1** < **1.0.0**.


<br>
<br>


<!-- Versioning Grammar Rules -->

## Versioning Grammar Rules 

[Table of Contents](#notebook_with_decorative_cover-table-of-contents)

```
		<VID> ::= <NORM-VID>
				 | <NORM-VID> "-" <PRE-RELEASE-VID>
				 | <NORM-VID> "+" <BUILD-METADATA-VID>
				 | <NORM-VID> "-" <PRE-RELEASE-VID> "+" <BUILD-METADATA-VID>

		<NORM-VID> ::= <MAJOR-VID> "." <MINOR-VID> "." <PATCH-VID>

		<MAJOR-VID> ::= <numeric identifier>

		<MINOR-VID> ::= <numeric identifier>

		<PATCH-VID> ::= <numeric identifier>

		<PRE-RELEASE-VID> ::= <dot-separated pre-release identifiers>

		<BUILD-METADATA-VID> ::= <dot-separated build identifiers>

		<dot-separated pre-release identifiers> ::= <pre-release identifier>
						          | <pre-release identifier> "." <dot-separated pre-release identifiers>

		<pre-release identifier> ::= <alphanumeric identifier>
					   | <numeric identifier>

		<dot-separated build identifiers> ::= <build identifier>
						    | <build identifier> "." <dot-separated build identifiers>

		<build identifier> ::= <alphanumeric identifier>
				     | <digits>

		<alphanumeric identifier> ::= <non-digit>
					    | <non-digit> <identifier characters>
					    | <identifier characters> <non-digit>
					    | <identifier characters> <non-digit> <identifier characters>

		<numeric identifier> ::= "0"
				       | <positive digit>
				       | <positive digit> <digits>

		<identifier characters> ::= <identifier character>
					  | <identifier character> <identifier characters>

		<identifier character> ::= <digit>
					 | <non-digit>

		<non-digit> ::= <letter>
			      | "-"

		<digits> ::= <digit>
			   | <digit> <digits>

		<digit> ::= "0"
			  | <positive digit>

		<positive digit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

		 
		<letter> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
			   | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
			   | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d"
			   | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n"
			   | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x"
			   | "y" | "z"
```

<br>
<br>

<a name="see-also"></a>

# See Also

[Table of Contents](#table-of-contents)

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

<a name="faq"></a>


# FAQ ❓

Here you can find the Frequently Asked Questions and Answers.

<br>
<br>

<a name="contact-us"></a>


# Contact us ☎️

For **more information** on <b>Readme Template</b>  
<span class="md-link"
      data-github="../CONTACT_US.md"
      data-doxygen="md_CONTACT_US.html">
  <a href="../CONTACT_US.md"><b>contact us</b></a>
</span>.


<br>
<br>

<a name="official-links"></a>

# Official Links

[Table of Contents](#table-of-contents)

* [SemVer](https://www.semver.org) – A complete guide to **Semanting Verioning**. 
* [Doxygen](https://www.doxygen.nl/index.html) – **Documentation generator** for source code.
* [GitHub](https://github.com) – **Hosting** and **collaboration platform** for **Git** repositories.
* [Git](https://git-scm.com) – **Version control** system to manage source code.
* [GNU Make](https://www.gnu.org/software/make/) – **Build automation tool** to compile projects.
<br>
<br>



