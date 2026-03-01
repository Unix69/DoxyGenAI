<div align="center">

  <h1>C_Linux</h1>
  
  <br>
  
  <!-- Badges -->
  <div align="bottom">
    <a href="https://github.com/Unix69/C_Linux/graphs/contributors">
      <img src="https://img.shields.io/github/contributors/Unix69/C_Linux" alt="contributors" />
    </a>
    <a href="">
      <img src="https://img.shields.io/github/last-commit/Unix69/C_Linux" alt="last update" />
    </a>
    <a href="https://github.com/Unix69/C_Linux/network/members">
      <img src="https://img.shields.io/github/forks/Unix69/C_Linux" alt="forks" />
    </a>
    <a href="https://github.com/Unix69/C_Linux/stargazers">
      <img src="https://img.shields.io/github/stars/Unix69/C_Linux" alt="stars"/>
    </a>
    <a href="https://github.com/Unix69/C_Linux/issues/">
      <img src="https://img.shields.io/github/issues/Unix69/C_Linux" alt="open issues" />
    </a>
    <a href="https://github.com/Unix69/C_Linux/blob/master/LICENSE.md">
      <img src="https://img.shields.io/github/license/Unix69/C_Linux.svg" alt="license" />
    </a>
  </div>

  <br>
  <br>

  <p>
    A set of <b>C example programs</b> showing the basic usage of <b>Unix system calls</b> related to <b>Filesystem</b>, <b>Processes</b> and <b>Threads</b> to learn about Unix-like filesystem manipulation and C multiprocess and multithread programming.  
  </p>
</div>

<br>
<br>
<br>



<a name="table-of-contents"></a>

### 📖 Table of Contents

- [C Unix & Standard Library Examples](#examples)
- [Getting Started](#getting-started)
- [License](#license)
- [Contributing](#contributing)
  - [Fork Project](#fork-project)
  - [Pull Request](#pull-request)
  - [Issue](#issue)
  - [Code Of Conduct](#code-of-conduct)
- [FAQ](#faq)
- [Authors](#authors)

<br>

---

<br>

### Summary

This collection of examples demonstrates:

- **Function pointers & generic programming** – dynamic invocation and flexible code structures.
- **File I/O with C Standard Library** – byte-wise and stream-based file operations.
- **Unix process management** – creation, synchronization, and termination of child processes.
- **Signals & IPC mechanisms** – using `kill()`, `pause()`, `pipe()`, and `wait()` for inter-process communication.
- **Multithreading & thread-safe operations** – concurrent processing of data, file I/O, and sorting using `pthread_create` and `pthread_join`.


<br>
<br>

<a id="examples"></a>
<section id="c-examples-preamble">
  <h2>📚 C Unix & Standard Library Examples</h2>

  <p>
    This collection of examples demonstrates key concepts in <strong>C programming</strong> on a <strong>Unix-like operating system</strong> using standard tools and libraries. All examples were developed using:
  </p>

  <ul>
    <li><strong>Language:</strong> C (C99/C11 standard)</li>
    <li><strong>OS:</strong> Linux / Unix-like environments</li>
    <li><strong>Toolchain:</strong> GCC, Make, POSIX-compliant libraries</li>
    <li><strong>Techniques demonstrated:</strong> Process creation and management, inter-process communication (IPC), file I/O, signals, threading, synchronization, assertion-based error checking</li>
    <li><strong>Libraries used:</strong> <code>&lt;stdio.h&gt;</code>, <code>&lt;stdlib.h&gt;</code>, <code>&lt;unistd.h&gt;</code>, <code>&lt;fcntl.h&gt;</code>, <code>&lt;pthread.h&gt;</code>, <code>&lt;assert.h&gt;</code>, <code>&lt;string.h&gt;</code></li>
    <li><strong>Programming techniques:</strong> Forking, wait/waitpid, pipes, signals, pause, kill, thread creation and joining, dynamic memory management, bubble sort in threads, concurrent file processing</li>
  </ul>

  <p>
    Below is a comprehensive list of the examples included in this folder, grouped by topic, with direct links to their detailed sections:
  </p>

  <h3>🧩 Function Pointers</h3>
  <ul>
    <li><a href="#c-func-pointer">C-Func-pointer</a> – Demonstrates function pointers in C, dynamic invocation, and generic programming using <code>void *</code>.</li>
  </ul>

  <h3>📄 Standard File I/O</h3>
  <ul>
    <li><a href="#c-std-file">C-STD-File</a> – Basic file input/output, copying files byte by byte, error handling, and EOF processing.</li>
  </ul>

  <h3>🖥️ Unix Process Management – Fork & Wait</h3>
  <ul>
    <li><a href="#c-unix-std-basic-fork">C-Unix-STD-Basic-Fork</a> – Basic process creation using <code>fork()</code>.</li>
    <li><a href="#c-unix-std-fork">C-Unix-STD-Fork</a> – Process creation and simple child execution.</li>
    <li><a href="#c-unix-std-fork-sleep">C-Unix-STD-Fork-Sleep</a> – Process sleeping and parent-child coordination.</li>
    <li><a href="#c-unix-std-fork-wait">C-Unix-STD-Fork-Wait</a> – Waiting for child processes using <code>wait()</code>.</li>
    <li><a href="#c-unix-std-fork-waitpid">C-Unix-STD-Fork-Waitpid</a> – Selective waiting with <code>waitpid()</code>.</li>
    <li><a href="#c-unix-std-fork-wait-precedence">C-Unix-STD-Fork-Wait-Precedence</a> – Controlling execution order of children.</li>
  </ul>

  <h3>🔄 Unix Executables & Directories</h3>
  <ul>
    <li><a href="#c-unix-std-copy-directorytree">C-Unix-STD-Copy-DirectoryTree</a> – Recursive directory copying using standard file I/O.</li>
    <li><a href="#c-unix-std-execl">C-Unix-STD-Execl</a> – Executing external programs with <code>execl()</code>.</li>
    <li><a href="#c-unix-std-execlp-system">C-Unix-STD-Execlp-System</a> – Executing external programs using <code>execlp()</code> and <code>system()</code>.</li>
    <li><a href="#c-unix-std-explore-file-directories">C-Unix-STD-Explore-File-Directories</a> – Directory exploration using <code>opendir()</code> and <code>readdir()</code>.</li>
  </ul>

  <h3>⚡ Signals & Inter-Process Communication</h3>
  <ul>
    <li><a href="#c-unix-std-kill">C-Unix-STD-Kill</a> – Sending signals to processes with <code>kill()</code>.</li>
    <li><a href="#c-unix-std-signal">C-Unix-STD-Signal</a> – Signal handling and custom handlers with <code>signal()</code>.</li>
    <li><a href="#c-unix-std-signal-fork">C-Unix-STD-Signal-Fork</a> – Combining signals with child processes.</li>
    <li><a href="#c-unix-std-signal-fork-kill">C-Unix-STD-Signal-Fork-Kill</a> – Parent-child signaling with <code>kill()</code>.</li>
    <li><a href="#c-unix-std-signal-fork-pause">C-Unix-STD-Signal-Fork-Pause</a> – Synchronization using <code>pause()</code>.</li>
    <li><a href="#c-unix-std-signal-fork-pause-kill">C-Unix-STD-Signal-Fork-Pause-Kill</a> – Controlled signaling using <code>pause()</code> and <code>kill()</code>.</li>
    <li><a href="#c-unix-std-signal-fork-pause-kill-file-wait">C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait</a> – File reading, signaling, and parent-child synchronization.</li>
    <li><a href="#c-unix-std-signal-fork-pause-kill-pipe">C-Unix-STD-Signal-Fork-Pause-Kill-Pipe</a> – Parent-child IPC via pipes with file streaming to stdout.</li>
    <li><a href="#c-unix-std-signal-fork-pause-kill-wait">C-Unix-STD-Signal-Fork-Pause-Kill-Wait</a> – Multi-child signaling with sequential wait synchronization.</li>
  </ul>

  <h3>🧵 Threads & Concurrent File Processing</h3>
  <ul>
    <li><a href="#c-unix-std-threads">C-Unix-STD-Threads</a> – Concurrent processing of file pairs using threads.</li>
    <li><a href="#c-unix-std-threads-files-assert">C-Unix-STD-Threads-Files-Assert</a> – Multithreaded file processing with bubble sort and assertion-based checks.</li>
  </ul>

  <p>
    Each example includes detailed explanations of the system calls, functions, and programming techniques used. They serve as a reference for:
  </p>
  <ul>
    <li>Process creation and management</li>
    <li>Inter-process communication (pipes, signals)</li>
    <li>File I/O and directory exploration</li>
    <li>Threading and synchronization</li>
    <li>Assertion-based error checking and debugging</li>
    <li>Concurrent algorithms (sorting, data processing)</li>
  </ul>


<br>

Let's start to see each example into detail. 

</section>


<br>
<br>


<a id="c-func-pointer"></a>
<section id="c-func-pointer">

  <h2>🧪 C-Func-pointer</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Func-pointer/main.c</code>
    </p>
    <a href="https://github.com/&lt;username&gt;/&lt;repo&gt;/blob/main/src/C-Func-pointer/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates the use of <strong>function pointers in C</strong>,
    showing how functions can be assigned to variables, passed around,
    and invoked dynamically at runtime.
  </p>
  <p>
    The goal is to understand:
  </p>
  <ul>
    <li>how to declare and use function pointers</li>
    <li>how to pass generic data using <code>void *</code></li>
    <li>how to build flexible and reusable logic</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program manages an integer array of fixed size using a set of functions
    operating on generic pointers.
  </p>

  <p>
    The execution flow is the following:
  </p>
  <ol>
    <li>
      <code>init()</code> dynamically allocates and initializes an integer array
      of size <code>dim</code> with all values set to zero
    </li>
    <li>
      Two function pointers are declared:
      <ul>
        <li><code>add</code> → points to <code>inc()</code></li>
        <li><code>dec</code> → points to <code>sub()</code></li>
      </ul>
    </li>
    <li>
      <code>inc()</code> increments each element of the array by a given value
    </li>
    <li>
      <code>sub()</code> decrements each element of the array by a given value
    </li>
    <li>
      <code>show()</code> prints the content of the array
    </li>
  </ol>

  <p>
    All data manipulation functions receive the array as a <code>void *</code>,
    demonstrating a <strong>generic programming approach</strong> in C.
  </p>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output operations</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/stdio" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>Dynamic memory allocation</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>&lt;string.h&gt;</code></td>
        <td>String manipulation utilities</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/string" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ Functions Used</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>malloc()</code></td>
        <td>Allocates memory dynamically</td>
        <td>
          <a href="https://en.cppreference.com/w/c/memory/malloc" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>printf()</code></td>
        <td>Prints formatted output</td>
        <td>
          <a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🧷 Function pointers</li>
    <li>🧬 Generic programming with <code>void *</code></li>
    <li>🧠 Indirect function invocation</li>
    <li>📦 Dynamic memory allocation</li>
    <li>♻️ Reusable and modular code</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>
      📘 <strong>Function Pointers in C:</strong>
      <a href="https://en.cppreference.com/w/c/language/pointer" target="_blank">
        cppreference – Pointers
      </a>
    </li>
  </ul>

</section>

<br>

<a id="c-std-file"></a>
<section id="c-std-file">

  <h2>🧪 C-STD-File</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-STD-File/main.c</code>
    </p>
    <a href="https://github.com/&lt;username&gt;/&lt;repo&gt;/blob/main/src/C-STD-File/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example shows how to perform <strong>basic file input/output using the C standard library</strong>.
    The program copies the content of a source file into a destination file, byte by byte.
  </p>
  <p>
    It introduces fundamental concepts such as file streams, error handling,
    and sequential file processing.
  </p>

  <h3>🛠️ Description</h3>
  <p>
    The program expects exactly two command-line arguments:
  </p>
  <ul>
    <li>the path of the source file to read</li>
    <li>the path of the destination file to write</li>
  </ul>

  <p>
    The execution flow is the following:
  </p>
  <ol>
    <li>
      Checks the number of command-line arguments
    </li>
    <li>
      Opens the source file in read mode using <code>fopen()</code>
    </li>
    <li>
      Opens (or creates) the destination file in write mode
    </li>
    <li>
      Reads characters one by one from the source file using <code>fgetc()</code>
    </li>
    <li>
      Writes each character to the destination file using <code>fputc()</code>
    </li>
  </ol>

  <p>
    The program stops copying when the <code>EOF</code> (End Of File) marker is reached.
    This demonstrates a simple and classic file copy algorithm using standard I/O.
  </p>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output and file streams</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/stdio" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>General utilities</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>&lt;assert.h&gt;</code></td>
        <td>Runtime assertions for error checking</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/assert" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ Standard Functions Used</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fopen()</code></td>
        <td>Opens a file stream</td>
        <td>
          <a href="https://en.cppreference.com/w/c/io/fopen" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>fgetc()</code></td>
        <td>Reads a character from a file</td>
        <td>
          <a href="https://en.cppreference.com/w/c/io/fgetc" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>fputc()</code></td>
        <td>Writes a character to a file</td>
        <td>
          <a href="https://en.cppreference.com/w/c/io/fputc" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>fprintf()</code></td>
        <td>Prints formatted output to a stream</td>
        <td>
          <a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>assert()</code></td>
        <td>Checks runtime conditions</td>
        <td>
          <a href="https://en.cppreference.com/w/c/error/assert" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>📂 File streams (<code>FILE *</code>)</li>
    <li>📝 Character-based file I/O</li>
    <li>⚠️ Basic error handling</li>
    <li>🧪 Runtime assertions</li>
    <li>📄 End Of File (<code>EOF</code>) handling</li>
  </ul>

  <h3>🔗 Related References</h3>
  <ul>
    <li>
      📘 <strong>C File I/O:</strong>
      <a href="https://en.cppreference.com/w/c/io" target="_blank">
        cppreference – C Input/Output
      </a>
    </li>
  </ul>

</section>

<br>

<a id="c-unix-std-basic-fork"></a>
<section id="c-unix-std-basic-fork">

  <h2>🧪 C-Unix-STD-Basic-Fork</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Basic-Fork/main.c</code>
    </p>
    <a href="https://github.com/&lt;username&gt;/&lt;repo&gt;/blob/main/src/C-Unix-STD-Basic-Fork/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates the <strong>basic behavior of the <code>fork()</code> system call</strong>
    and how a process is <strong>duplicated</strong> into a parent and a child process.
  </p>
  <p>
    The goal is to understand:
  </p>
  <ul>
    <li>how to distinguish parent and child processes</li>
    <li>how execution flow is duplicated</li>
    <li>how concurrent processes produce output</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program executes a decreasing <code>for</code> loop (<code>i = 2 → 1</code>).
    At each iteration:
  </p>
  <ol>
    <li>the <code>fork()</code> system call is invoked</li>
    <li>the <strong>parent process</strong> receives a value greater than <code>0</code></li>
    <li>the <strong>child process</strong> receives <code>0</code></li>
    <li>
      based on the return value:
      <ul>
        <li>the parent prints <code>i</code></li>
        <li>the child prints <code>-i</code></li>
      </ul>
    </li>
  </ol>

  <p>
    Since <code>fork()</code> duplicates the current process:
  </p>
  <ul>
    <li>after the first iteration there are <strong>2 running processes</strong></li>
    <li>after the second iteration there are <strong>4 running processes</strong></li>
  </ul>

  <p>
    The order of the printed output is <strong>non-deterministic</strong>,
    because it depends on the operating system scheduler.
  </p>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>Standard utility functions</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output</td>
        <td>
          <a href="https://en.cppreference.com/w/c/header/stdio" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>POSIX process control</td>
        <td>
          <a href="https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/unistd.h.html" target="_blank">
            Open Group
          </a>
        </td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fork()</code></td>
        <td>Creates a new process by duplicating the caller</td>
        <td>
          <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">
            man7.org
          </a>
        </td>
      </tr>
      <tr>
        <td><code>printf()</code></td>
        <td>Writes formatted output to stdout</td>
        <td>
          <a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">
            cppreference
          </a>
        </td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Process creation</li>
    <li>👨‍👦 Parent vs child execution</li>
    <li>🔁 Concurrent execution</li>
    <li>🎲 Non-deterministic output</li>
    <li>📈 Exponential process growth</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>
      📘 <strong>POSIX fork() Reference:</strong>
      <a href="https://pubs.opengroup.org/onlinepubs/9699919799/functions/fork.html" target="_blank">
        Open Group Specification
      </a>
    </li>
  </ul>

</section>

<br>

<a id="c-unix-std-copy-directorytree"></a>
<section id="c-unix-std-copy-directorytree">

  <h2>🧪 C-Unix-STD-Copy-DirectoryTree</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Copy-DirectoryTree/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Copy-DirectoryTree/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>recursive copying of a directory tree using Unix system calls</strong>.
    It shows how to duplicate all files and subdirectories from a source directory to a destination directory.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how to traverse directories recursively</li>
    <li>how to handle files and directories differently</li>
    <li>how low-level file I/O works in Unix</li>
    <li>how to implement robust error handling</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program expects exactly two command-line arguments:
  </p>
  <ul>
    <li>the path of the source directory</li>
    <li>the path of the destination directory</li>
  </ul>
  <p>Execution flow:</p>
  <ol>
    <li>Validate argument count using <code>assert()</code>.</li>
    <li>Retrieve file status of source and destination using <code>lstat()</code>.</li>
    <li>Check that both paths are directories using <code>S_ISDIR()</code>.</li>
    <li>Invoke the recursive <code>copia()</code> function:
      <ul>
        <li>Open source and destination directories with <code>opendir()</code>.</li>
        <li>Iterate over directory entries using <code>readdir()</code>, skipping <code>.</code> and <code>..</code>.</li>
        <li>Build full paths for each entry with <code>sprintf()</code>.</li>
        <li>Check entry type using <code>lstat()</code>:
          <ul>
            <li>If a file, copy its contents using <code>open()</code>, <code>read()</code>, and <code>write()</code>.</li>
            <li>If a directory, create it using <code>mkdir()</code> and recursively call <code>copia()</code>.</li>
          </ul>
        </li>
        <li>Close directory streams with <code>closedir()</code>.</li>
      </ul>
    </li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard I/O for <code>fprintf()</code></td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>Standard utilities, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;sys/types.h&gt;</code></td>
        <td>Data types for system calls</td>
        <td><a href="https://man7.org/linux/man-pages/man2/stat.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;sys/stat.h&gt;</code></td>
        <td>File status and mode macros (<code>S_ISDIR</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/stat.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>Unix standard functions (<code>read, write, close</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/read.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;dirent.h&gt;</code></td>
        <td>Directory handling (<code>opendir, readdir, closedir</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man3/readdir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;fcntl.h&gt;</code></td>
        <td>File control flags (<code>O_RDONLY, O_WRONLY, O_CREAT</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/open.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;assert.h&gt;</code></td>
        <td>Runtime assertions</td>
        <td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>lstat()</code></td>
        <td>Retrieve file or directory status</td>
        <td><a href="https://man7.org/linux/man-pages/man2/lstat.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>S_ISDIR()</code></td>
        <td>Check if path is a directory</td>
        <td><a href="https://man7.org/linux/man-pages/man2/stat.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>opendir()</code></td>
        <td>Open a directory stream</td>
        <td><a href="https://man7.org/linux/man-pages/man3/opendir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>readdir()</code></td>
        <td>Read entries from a directory</td>
        <td><a href="https://man7.org/linux/man-pages/man3/readdir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>closedir()</code></td>
        <td>Close a directory stream</td>
        <td><a href="https://man7.org/linux/man-pages/man3/closedir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>open()</code></td>
        <td>Open a file descriptor</td>
        <td><a href="https://man7.org/linux/man-pages/man2/open.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>read()</code></td>
        <td>Read bytes from a file descriptor</td>
        <td><a href="https://man7.org/linux/man-pages/man2/read.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>write()</code></td>
        <td>Write bytes to a file descriptor</td>
        <td><a href="https://man7.org/linux/man-pages/man2/write.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>mkdir()</code></td>
        <td>Create a new directory</td>
        <td><a href="https://man7.org/linux/man-pages/man2/mkdir.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>sprintf()</code></td>
        <td>Build full file paths as strings</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>assert()</code></td>
        <td>Runtime condition checks</td>
        <td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>fprintf()</code></td>
        <td>Print formatted error messages to <code>stderr</code></td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>📂 Recursive directory traversal</li>
    <li>📝 Low-level file I/O with <code>open/read/write</code></li>
    <li>⚠️ Error handling with <code>fprintf()</code>, <code>assert()</code>, and <code>exit()</code></li>
    <li>🔄 Preserving directory structure</li>
    <li>🧪 Runtime validation of command-line arguments</li>
    <li>🔁 Recursion for nested directories</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>Unix Directory Handling:</strong> <a href="https://man7.org/linux/man-pages/man3/readdir.3.html" target="_blank">opendir/readdir/closedir</a></li>
    <li>📘 <strong>Unix File I/O:</strong> <a href="https://man7.org/linux/man-pages/man2/read.2.html" target="_blank">read/write/open</a></li>
    <li>📘 <strong>C File I/O:</strong> <a href="https://en.cppreference.com/w/c/io" target="_blank">cppreference – C Input/Output</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-execl"></a>
<section id="c-unix-std-execl">

  <h2>🧪 C-Unix-STD-Execl</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Execl/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Execl/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates the <strong>use of the <code>execl()</code> system call</strong>
    to replace the current process image with a new program.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how <code>execl()</code> replaces the current process</li>
    <li>how execution flow stops after a successful <code>execl()</code></li>
    <li>the effect on program output when <code>execl()</code> fails</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program expects one command-line argument specifying the program to execute:
  </p>
  <ul>
    <li>Print the current process ID and increment a counter.</li>
    <li>Call <code>execl()</code> with the provided program path.</li>
    <li>If <code>execl()</code> succeeds, the new program replaces the current process and the next <code>fprintf()</code> is not executed.</li>
    <li>If <code>execl()</code> fails, an error message is printed and the program exits with <code>return 1</code>.</li>
  </ul>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output functions</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>General utilities, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>POSIX system calls, <code>execl(), getpid()</code></td>
        <td><a href="https://man7.org/linux/man-pages/man3/execl.3.html" target="_blank">man7.org</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>execl()</code></td>
        <td>Replaces current process image with a new program</td>
        <td><a href="https://man7.org/linux/man-pages/man3/execl.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>getpid()</code></td>
        <td>Returns the process ID of the current process</td>
        <td><a href="https://man7.org/linux/man-pages/man2/getpid.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>fprintf()</code></td>
        <td>Print formatted output to a stream (stdout or stderr)</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔁 Process replacement with <code>execl()</code></li>
    <li>👀 Execution flow stops after successful <code>execl()</code></li>
    <li>⚠️ Handling execl failure</li>
    <li>📄 Process identification with <code>getpid()</code></li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX execl():</strong> <a href="https://man7.org/linux/man-pages/man3/execl.3.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-execlp-system"></a>
<section id="c-unix-std-execlp-system">

  <h2>🧪 C-Unix-STD-Execlp-System</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Execlp-System/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Execlp-System/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>process creation and execution using <code>fork()</code>, <code>system()</code>, and <code>execlp()</code></strong>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how <code>fork()</code> creates concurrent processes</li>
    <li>how <code>system()</code> can execute shell commands</li>
    <li>how <code>execlp()</code> replaces the process image</li>
    <li>how parent and child processes interact</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program executes nested loops with process creation:
  </p>
  <ol>
    <li>Call <code>fork()</code> to create the first child.</li>
    <li>For <code>i = 0</code> to <code>1</code>:
      <ul>
        <li>If in the parent process, build a command string and execute it using <code>system()</code>.</li>
        <li>If in the child process, build a string and execute it using <code>execlp()</code> with <code>echo</code>.</li>
      </ul>
    </li>
    <li>The <code>execlp()</code> calls replace the child process image with <code>echo</code>, while <code>system()</code> runs in the parent process.</li>
    <li>This demonstrates concurrent execution and process replacement within the same loop.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output functions</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>General utilities, <code>system()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>POSIX system calls (<code>fork()</code>, <code>execlp()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man3/execlp.3.html" target="_blank">man7.org</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fork()</code></td>
        <td>Create a new child process</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>execlp()</code></td>
        <td>Replace current process image with a new program found in PATH</td>
        <td><a href="https://man7.org/linux/man-pages/man3/execlp.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>system()</code></td>
        <td>Execute shell command in a separate process</td>
        <td><a href="https://man7.org/linux/man-pages/man3/system.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>sprintf()</code></td>
        <td>Format string into buffer for command execution</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Process creation and concurrency with <code>fork()</code></li>
    <li>🔁 Process replacement with <code>execlp()</code></li>
    <li>💻 Shell command execution with <code>system()</code></li>
    <li>⚠️ Parent vs child process execution control</li>
    <li>📄 Demonstrates interaction between multiple processes in a loop</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX fork():</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>POSIX execlp():</strong> <a href="https://man7.org/linux/man-pages/man3/execlp.3.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>system():</strong> <a href="https://man7.org/linux/man-pages/man3/system.3.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-explore-directories"></a>
<section id="c-unix-std-explore-directories">

  <h2>🧪 C-Unix-STD-Explore-Directories</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Explore-Directories/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Explore-Directories/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>recursive exploration of directories</strong> in a file system.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how to navigate directories using <code>opendir()</code> and <code>readdir()</code></li>
    <li>how to distinguish files and directories using <code>lstat()</code></li>
    <li>how recursion can be applied to traverse an entire directory tree</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program expects a single command-line argument specifying the root directory:
  </p>
  <ol>
    <li>Check if the provided path exists and is a directory using <code>lstat()</code>.</li>
    <li>Call a recursive function <code>funzione()</code> to explore the directory tree.</li>
    <li>Inside the recursive function:
      <ul>
        <li>Open the directory with <code>opendir()</code>.</li>
        <li>Iterate over all entries with <code>readdir()</code>.</li>
        <li>For files, print the full path.</li>
        <li>For directories, print the path and recursively explore its contents.</li>
      </ul>
    </li>
    <li>Close the directory after traversal with <code>closedir()</code>.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Input/output functions</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>General utilities, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>POSIX system calls (<code>lstat()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/lstat.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;sys/stat.h&gt;</code></td>
        <td>File status information</td>
        <td><a href="https://en.cppreference.com/w/c/sys/stat" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;dirent.h&gt;</code></td>
        <td>Directory stream handling</td>
        <td><a href="https://man7.org/linux/man-pages/man3/readdir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;string.h&gt;</code></td>
        <td>String manipulation functions</td>
        <td><a href="https://en.cppreference.com/w/c/string" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>lstat()</code></td>
        <td>Get information about a file or directory</td>
        <td><a href="https://man7.org/linux/man-pages/man2/lstat.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>opendir()</code></td>
        <td>Open a directory stream</td>
        <td><a href="https://man7.org/linux/man-pages/man3/opendir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>readdir()</code></td>
        <td>Read the next entry in a directory</td>
        <td><a href="https://man7.org/linux/man-pages/man3/readdir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>closedir()</code></td>
        <td>Close a directory stream</td>
        <td><a href="https://man7.org/linux/man-pages/man3/closedir.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>fprintf()</code></td>
        <td>Print formatted output to stdout/stderr</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>📂 Directory traversal using <code>opendir()/readdir()</code></li>
    <li>📝 Differentiating files and directories</li>
    <li>🔁 Recursive algorithms</li>
    <li>⚠️ Basic error handling in file systems</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX Directory Operations:</strong> <a href="https://man7.org/linux/man-pages/man3/readdir.3.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-fork"></a>
<section id="c-unix-std-fork">

  <h2>🧪 C-Unix-STD-Fork</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Fork/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Fork/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>process creation using <code>fork()</code> and semaphores</strong> to control output order.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how multiple child processes can be created concurrently</li>
    <li>how to use semaphores to synchronize process output</li>
    <li>how process execution order can be controlled</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program reads a string from stdin and creates one child process per character:
  </p>
  <ol>
    <li>Initialize a semaphore to zero.</li>
    <li>For each character, create a child process using <code>fork()</code>.</li>
    <li>Each child waits on the semaphore (<code>sem_wait()</code>) before printing its character.</li>
    <li>The parent posts to the semaphore (<code>sem_post()</code>) sequentially to allow children to print in order.</li>
    <li>Child processes exit after printing, ensuring ordered output.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>General utilities, memory allocation, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>POSIX process control (<code>fork()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;semaphore.h&gt;</code></td>
        <td>POSIX semaphores for process synchronization</td>
        <td><a href="https://man7.org/linux/man-pages/man7/sem_overview.7.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;string.h&gt;</code></td>
        <td>String manipulation (<code>strlen()</code>, <code>strdup()</code>)</td>
        <td><a href="https://en.cppreference.com/w/c/string" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fork()</code></td>
        <td>Create a new child process</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>sem_init()</code></td>
        <td>Initialize semaphore</td>
        <td><a href="https://man7.org/linux/man-pages/man3/sem_init.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>sem_wait()</code></td>
        <td>Wait (decrement) on semaphore</td>
        <td><a href="https://man7.org/linux/man-pages/man3/sem_wait.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>sem_post()</code></td>
        <td>Signal (increment) semaphore</td>
        <td><a href="https://man7.org/linux/man-pages/man3/sem_post.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>printf()</code></td>
        <td>Output character to stdout</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Process creation with <code>fork()</code></li>
    <li>🔁 Process synchronization using semaphores</li>
    <li>📝 Ordered output from concurrent processes</li>
    <li>⚠️ Proper use of <code>exit()</code> in child processes</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX fork():</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>POSIX semaphores:</strong> <a href="https://man7.org/linux/man-pages/man7/sem_overview.7.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-fork-sleep"></a>
<section id="c-unix-std-fork-sleep">

  <h2>🧪 C-Unix-STD-Fork-Sleep</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Fork-Sleep/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Fork-Sleep/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>nested process creation using <code>fork()</code> and controlled termination with <code>sleep()</code></strong>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how multiple levels of processes can be spawned</li>
    <li>how to differentiate "leaf" processes</li>
    <li>how <code>sleep()</code> can be used to control process timing and termination</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program expects two command-line arguments: number of iterations <code>n</code> and sleep time <code>t</code>:
  </p>
  <ol>
    <li>Loop <code>i = 0 → n-1</code>, creating child processes with <code>fork()</code>.</li>
    <li>Within the loop, if in the parent process, another <code>fork()</code> may be called to create nested children.</li>
    <li>After all forks, the process sleeps for <code>t</code> seconds.</li>
    <li>After waking, the leaf process prints a termination message.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Input/output functions</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>General utilities, <code>atoi()</code>, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>POSIX system calls, <code>fork()</code>, <code>sleep()</code></td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;sys/wait.h&gt;</code></td>
        <td>Waiting for process termination</td>
        <td><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;assert.h&gt;</code></td>
        <td>Runtime assertions</td>
        <td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fork()</code></td>
        <td>Create a new child process</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>sleep()</code></td>
        <td>Pause process execution for a specified time</td>
        <td><a href="https://man7.org/linux/man-pages/man3/sleep.3.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>printf()</code></td>
        <td>Output to stdout</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>assert()</code></td>
        <td>Verify runtime conditions</td>
        <td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Nested process creation with <code>fork()</code></li>
    <li>⏳ Process timing control with <code>sleep()</code></li>
    <li>⚠️ Parent vs leaf process identification</li>
    <li>📄 Controlled process termination</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX fork():</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>sleep():</strong> <a href="https://man7.org/linux/man-pages/man3/sleep.3.html" target="_blank">man7.org</a></li>
  </ul>

</section>


<br>



<a id="c-unix-std-fork-wait"></a>
<section id="c-unix-std-fork-wait">

  <h2>🧪 C-Unix-STD-Fork-Wait</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Fork-Wait/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Fork-Wait/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>process creation with <code>fork()</code> and parent-child synchronization using <code>wait()</code></strong>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how the parent waits for child processes to complete before continuing</li>
    <li>how to pass data from the parent to children using memory arrays</li>
    <li>how sequential output can be enforced using <code>wait()</code></li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program expects a single command-line argument <code>n</code> for the number of integers:
  </p>
  <ol>
    <li>Allocate an array of size <code>n</code> dynamically using <code>malloc()</code>.</li>
    <li>Read <code>n</code> integers from the user into the array.</li>
    <li>Loop over the array, and for each element:
      <ul>
        <li>Call <code>fork()</code> to create a child process.</li>
        <li>In the parent process:
          <ul>
            <li>Call <code>wait(NULL)</code> to wait for the child to finish.</li>
            <li>Print the corresponding integer from the array.</li>
            <li>Exit with the child index as exit code.</li>
          </ul>
        </li>
      </ul>
    </li>
    <li>Child processes exit immediately after creation.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>Memory allocation (<code>malloc()</code>), <code>atoi()</code>, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>Process creation (<code>fork()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;sys/wait.h&gt;</code></td>
        <td>Waiting for child process termination (<code>wait()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;assert.h&gt;</code></td>
        <td>Runtime assertions</td>
        <td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fork()</code></td>
        <td>Create child processes</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>wait()</code></td>
        <td>Wait for a child process to terminate</td>
        <td><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>malloc()</code></td>
        <td>Allocate dynamic memory for the integer array</td>
        <td><a href="https://en.cppreference.com/w/c/memory/malloc" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>exit()</code></td>
        <td>Terminate a process with a specific exit code</td>
        <td><a href="https://en.cppreference.com/w/c/program/exit" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Process creation and parent-child hierarchy</li>
    <li>⏳ Sequential execution of child processes using <code>wait()</code></li>
    <li>📝 Passing and printing data via shared memory arrays</li>
    <li>⚠️ Proper termination of child processes</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX fork():</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>POSIX wait():</strong> <a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<a id="c-unix-std-fork-wait-precedence"></a>
<section id="c-unix-std-fork-wait-precedence">

  <h2>🧪 C-Unix-STD-Fork-Wait-Precedence</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Fork-Wait-Precedence/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Fork-Wait-Precedence/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>process creation with multiple <code>fork()</code> calls and <code>wait()</code> to enforce execution precedence</strong>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how a complex tree of processes can be spawned</li>
    <li>how <code>wait()</code> controls which child completes before the parent proceeds</li>
    <li>how to trace parent-child relationships and execution order</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program creates a complex hierarchy of child processes:
  </p>
  <ol>
    <li>Parent creates child P1 with <code>fork()</code>. P1 prints its PID and exits.</li>
    <li>The parent waits for P1 to finish using <code>wait()</code>.</li>
    <li>Parent sequentially spawns P2, P3, … P12 with additional <code>fork()</code> calls, sometimes nested.</li>
    <li>Each child prints its PID, parent PID, and an iteration index, then exits.</li>
    <li>The use of <code>wait()</code> ensures that the parent continues only after specific children terminate, enforcing precedence.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>Utilities, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>Process creation (<code>fork()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;sys/wait.h&gt;</code></td>
        <td>Process termination synchronization (<code>wait()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;assert.h&gt;</code></td>
        <td>Runtime assertions</td>
        <td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fork()</code></td>
        <td>Create child processes in sequence and nested hierarchies</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>wait()</code></td>
        <td>Wait for specific child process to terminate, enforcing execution order</td>
        <td><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>printf()</code></td>
        <td>Print process information</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>exit()</code></td>
        <td>Terminate a process with a status code</td>
        <td><a href="https://en.cppreference.com/w/c/program/exit" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Nested and sequential process creation</li>
    <li>⏳ Controlling execution precedence using <code>wait()</code></li>
    <li>📄 Tracking PID and PPID relationships</li>
    <li>⚠️ Proper child process termination to prevent zombies</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX fork():</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>POSIX wait():</strong> <a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-fork-waitpid"></a>
<section id="c-unix-std-fork-waitpid">

  <h2>🧪 C-Unix-STD-Fork-Waitpid</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Fork-Waitpid/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Fork-Waitpid/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>process creation using <code>fork()</code> and selective waiting using <code>waitpid()</code></strong>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how to create multiple child processes</li>
    <li>how <code>waitpid()</code> can wait for specific child processes instead of any child</li>
    <li>how to handle process termination selectively</li>
  </ul>

  <h3>🛠️ Description</h3>
  <p>
    The program creates <code>N</code> child processes in a loop:
  </p>
  <ol>
    <li>For each child, call <code>fork()</code> and store the child PID in an array.</li>
    <li>In child processes, immediately exit with <code>EXIT_SUCCESS</code>.</li>
    <li>After creating children, the parent selectively waits for children with index > <code>M</code> using <code>waitpid()</code>.</li>
    <li>This demonstrates control over which child processes to wait for and allows partial concurrent execution.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>&lt;stdio.h&gt;</code></td>
        <td>Standard input/output</td>
        <td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;stdlib.h&gt;</code></td>
        <td>General utilities, <code>exit()</code></td>
        <td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td>
      </tr>
      <tr>
        <td><code>&lt;unistd.h&gt;</code></td>
        <td>Process creation (<code>fork()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>&lt;sys/wait.h&gt;</code></td>
        <td>Selective waiting for child processes (<code>waitpid()</code>)</td>
        <td><a href="https://man7.org/linux/man-pages/man2/waitpid.2.html" target="_blank">man7.org</a></td>
      </tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Role</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>fork()</code></td>
        <td>Create child processes</td>
        <td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>waitpid()</code></td>
        <td>Wait for a specific child process to terminate</td>
        <td><a href="https://man7.org/linux/man-pages/man2/waitpid.2.html" target="_blank">man7.org</a></td>
      </tr>
      <tr>
        <td><code>exit()</code></td>
        <td>Terminate a process</td>
        <td><a href="https://en.cppreference.com/w/c/program/exit" target="_blank">cppreference</a></td>
      </tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Multiple child process creation</li>
    <li>🧩 Selective waiting using <code>waitpid()</code></li>
    <li>⚠️ Preventing zombie processes</li>
    <li>⏱️ Partial concurrency control</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>POSIX fork():</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>POSIX waitpid():</strong> <a href="https://man7.org/linux/man-pages/man2/waitpid.2.html" target="_blank">man7.org</a></li>
  </ul>

</section>


<br>


<a id="c-unix-std-signal-fork-pause-kill-pipe"></a>
<section id="c-unix-std-signal-fork-pause-kill-pipe">

  <h2>🧪 C-Unix-STD-Signal-Fork-Pause-Kill-Pipe</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal-Fork-Pause-Kill-Pipe/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal-Fork-Pause-Kill-Pipe/main.c"
       target="_blank"
       style="display:inline-block;padding:6px 14px;border-radius:6px;background:#24292f;color:white;text-decoration:none;font-weight:600;font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>parent-child communication using a pipe</strong>, where the child reads a file and sends its content to the parent through the pipe.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>How to create a pipe for IPC between parent and child</li>
    <li>How a child can write data to a pipe and parent can read it</li>
    <li>How to coordinate file I/O with process communication</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Create a pipe using <code>pipe()</code> for IPC.</li>
    <li>Fork a child process:
      <ul>
        <li>Child closes the read-end of the pipe.</li>
        <li>Opens <code>testo.txt</code> and reads its content.</li>
        <li>Writes the content to the pipe.</li>
      </ul>
    </li>
    <li>Parent process closes the write-end of the pipe.</li>
    <li>Parent reads from the pipe and writes the content to stdout.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Header</th><th>Description</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;unistd.h&gt;</code></td><td>fork, pipe, read, write</td><td><a href="https://man7.org/linux/man-pages/man2/pipe.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;fcntl.h&gt;</code></td><td>File open/read</td><td><a href="https://man7.org/linux/man-pages/man2/open.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>Memory allocation, exit</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;stdio.h&gt;</code></td><td>File I/O and stdout</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;assert.h&gt;</code></td><td>Error checking</td><td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>fork()</code></td><td>Create child process</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>pipe()</code></td><td>Create IPC pipe</td><td><a href="https://man7.org/linux/man-pages/man2/pipe.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>read()</code>, <code>write()</code></td><td>Read/write through pipe and file</td><td><a href="https://man7.org/linux/man-pages/man2/read.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>close()</code></td><td>Close pipe ends</td><td><a href="https://man7.org/linux/man-pages/man2/close.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>exit()</code></td><td>Terminate a process</td><td><a href="https://en.cppreference.com/w/c/program/exit" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>📡 Parent-child IPC via pipe</li>
    <li>👨‍👦 Coordinated file read and stdout output</li>
    <li>🔁 Streaming data between processes using pipe</li>
    <li>⚠️ Ensuring proper pipe closure to prevent deadlocks</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">POSIX fork()</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/pipe.2.html" target="_blank">POSIX pipe()</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/read.2.html" target="_blank">POSIX read()</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/write.2.html" target="_blank">POSIX write()</a></li>
  </ul>

</section>


<br>

<a id="c-unix-std-signal-fork-pause-kill-wait"></a>
<section id="c-unix-std-signal-fork-pause-kill-wait">

  <h2>🧪 C-Unix-STD-Signal-Fork-Pause-Kill-Wait</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal-Fork-Pause-Kill-Wait/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal-Fork-Pause-Kill-Wait/main.c"
       target="_blank"
       style="display:inline-block;padding:6px 14px;border-radius:6px;background:#24292f;color:white;text-decoration:none;font-weight:600;font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>two-child signal-based communication with parent synchronization using <code>wait()</code></strong>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>How to use signals (<code>SIGUSR1</code>, <code>SIGUSR2</code>) for inter-process communication</li>
    <li>How to synchronize parent with multiple children using <code>wait()</code></li>
    <li>How to coordinate sequential execution of child processes</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Fork two child processes.</li>
    <li>Child processes pause until receiving their respective signal (<code>SIGUSR1</code> or <code>SIGUSR2</code>).</li>
    <li>Parent sends signals in a controlled order and waits for child termination using <code>wait()</code>.</li>
    <li>This ensures orderly execution and prevents zombie processes.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Header</th><th>Description</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;stdio.h&gt;</code></td><td>Standard input/output</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>Exit, general utilities</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;unistd.h&gt;</code></td><td>fork(), pause()</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;signal.h&gt;</code></td><td>Signal handling</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;sys/wait.h&gt;</code></td><td>wait() for child processes</td><td><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>fork()</code></td><td>Create child processes</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>signal()</code></td><td>Install signal handlers</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>pause()</code></td><td>Wait for a signal</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>kill()</code></td><td>Send signal to child</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>wait()</code></td><td>Wait for child termination</td><td><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">man7.org</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Parent-child signaling with <code>SIGUSR1</code>/<code>SIGUSR2</code></li>
    <li>⏱️ Synchronizing parent with children using <code>wait()</code></li>
    <li>⚠️ Preventing zombie processes</li>
    <li>🧩 Coordinated sequential execution</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">POSIX signal()</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/wait.2.html" target="_blank">POSIX wait()</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-kill"></a>
<section id="c-unix-std-kill">

  <h2>🧪 C-Unix-STD-Kill</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Kill/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Kill/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This program demonstrates the use of the <strong><code>kill()</code> system call</strong>
    to send signals to a specific process based on command-line arguments.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how to target a process by PID</li>
    <li>how to send different signals (<code>SIGUSR1</code>, <code>SIGUSR2</code>, <code>SIGINT</code>)</li>
    <li>how command-line arguments can control signal behavior</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Expect exactly two command-line arguments: target PID and a command string.</li>
    <li>Compare the command string:
      <ul>
        <li><code>somma</code> → send <code>SIGUSR2</code></li>
        <li><code>differenza</code> → send <code>SIGUSR1</code></li>
        <li><code>fine</code> → send <code>SIGINT</code></li>
      </ul>
    </li>
    <li>If the command is invalid, print an error message.</li>
    <li>Uses <code>kill(pid, signal)</code> to notify the target process.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr>
        <th>Header</th>
        <th>Description</th>
        <th>Reference</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;signal.h&gt;</code></td><td>Signal handling and sending (<code>kill()</code>)</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>Conversion (<code>atoi()</code>)</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;unistd.h&gt;</code></td><td>Process primitives</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;string.h&gt;</code></td><td>String comparison (<code>strcmp()</code>)</td><td><a href="https://en.cppreference.com/w/c/string/byte/strcmp" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;assert.h&gt;</code></td><td>Runtime assertion to check argument count</td><td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>kill()</code></td><td>Send a signal to a process by PID</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>atoi()</code></td><td>Convert string to integer (PID)</td><td><a href="https://en.cppreference.com/w/c/string/byte/atoi" target="_blank">cppreference</a></td></tr>
      <tr><td><code>strcmp()</code></td><td>Compare command strings</td><td><a href="https://en.cppreference.com/w/c/string/byte/strcmp" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>🔀 Process targeting by PID</li>
    <li>⚡ Sending signals to control remote process behavior</li>
    <li>⚠️ Handling invalid commands safely</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>kill() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-signal"></a>
<section id="c-unix-std-signal">

  <h2>🧪 C-Unix-STD-Signal</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    Demonstrates <strong>signal handling using <code>signal()</code> and <code>pause()</code></strong>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>how to handle multiple signals (<code>SIGUSR1</code>, <code>SIGUSR2</code>, <code>SIGINT</code>)</li>
    <li>how a process can react to external signals</li>
    <li>using <code>pause()</code> to wait for signals</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Set up handlers for <code>SIGUSR1</code>, <code>SIGUSR2</code>, <code>SIGINT</code> using <code>signal()</code>.</li>
    <li>Read two integers from the user.</li>
    <li>Enter an infinite loop calling <code>pause()</code> to wait for signals.</li>
    <li>When a signal is received:
      <ul>
        <li><code>SIGUSR1</code>: print the difference of the two integers.</li>
        <li><code>SIGUSR2</code>: print the sum of the two integers.</li>
        <li><code>SIGINT</code>: terminate the process.</li>
      </ul>
    </li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Header</th><th>Description</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;signal.h&gt;</code></td><td>Signal handling (<code>signal()</code>)</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;stdio.h&gt;</code></td><td>Input/output</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>General utilities (<code>exit()</code>)</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;unistd.h&gt;</code></td><td>Pause and process control</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>signal()</code></td><td>Install a handler for a specific signal</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>pause()</code></td><td>Wait until a signal is received</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>scanf()</code></td><td>Read integers from user</td><td><a href="https://en.cppreference.com/w/c/io/fscanf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>printf()</code></td><td>Print results</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>⚡ Signal handling</li>
    <li>⏳ Waiting for signals using <code>pause()</code></li>
    <li>📝 Dynamic reaction to external events</li>
    <li>⚠️ Graceful termination via signals</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>signal() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>pause() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-signal-fork"></a>
<section id="c-unix-std-signal-fork">

  <h2>🧪 C-Unix-STD-Signal-Fork</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal-Fork/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal-Fork/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    Demonstrates the combination of <strong>fork() and signal handling</strong>,
    showing how a parent can control child processes using signals.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>creating multiple child processes with <code>fork()</code></li>
    <li>sending signals to children to trigger handlers</li>
    <li>coordinating execution between parent and children</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Accept exactly one command-line argument <code>n</code>, the number of child processes.</li>
    <li>Install a signal handler <code>manager()</code> for <code>SIGUSR1</code> in children.</li>
    <li>Loop <code>n</code> times:
      <ul>
        <li>fork a child process</li>
        <li>child calls <code>pause()</code> and waits for a signal</li>
        <li>parent sleeps 2 seconds, prints info, then sends <code>SIGUSR1</code> to the child</li>
      </ul>
    </li>
    <li>Children print a message when receiving <code>SIGUSR1</code> and exit.</li>
    <li>Parent continues to the next child.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Header</th><th>Description</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;signal.h&gt;</code></td><td>Signal handling</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;unistd.h&gt;</code></td><td>Process control and fork</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;stdio.h&gt;</code></td><td>Input/output</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>Memory allocation, exit</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;assert.h&gt;</code></td><td>Runtime checks</td><td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>fork()</code></td><td>Create a child process</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>signal()</code></td><td>Assign handler to <code>SIGUSR1</code></td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>pause()</code></td><td>Wait until a signal arrives</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>kill()</code></td><td>Parent sends signal to child</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>printf()</code></td><td>Output messages to stdout</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>👶 Child processes with fork()</li>
    <li>⚡ Signal communication parent → child</li>
    <li>⏳ Synchronized execution using pause() and sleep()</li>
    <li>📝 Process info reporting via signals</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>fork() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>signal() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>pause() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></li>
  </ul>

</section>


<br>

<a id="c-unix-std-signal-fork-kill"></a>
<section id="c-unix-std-signal-fork-kill">

  <h2>🧪 C-Unix-STD-Signal-Fork-Kill</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal-Fork-Kill/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal-Fork-Kill/main.c"
       target="_blank"
       style="display:inline-block;
              padding:6px 14px;
              border-radius:6px;
              background:#24292f;
              color:white;
              text-decoration:none;
              font-weight:600;
              font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    Demonstrates a <strong>bidirectional signal exchange between parent and child processes</strong>
    combined with <code>fork()</code> and <code>kill()</code>.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>parent-child communication using signals</li>
    <li>how children can respond to signals and reply to parent</li>
    <li>looping signal interactions in a controlled sequence</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Parent sets up handlers for <code>SIGUSR1</code>, <code>SIGUSR2</code>, <code>SIGINT</code>.</li>
    <li>Parent forks a single child process.</li>
    <li>Child enters an infinite loop, waiting for signals using <code>pause()</code> and reacts:
      <ul>
        <li><code>SIGUSR1</code>: send <code>SIGUSR2</code> to parent</li>
        <li><code>SIGUSR2</code>: send <code>SIGUSR1</code> to parent</li>
        <li><code>SIGINT</code>: send <code>SIGINT</code> to parent and terminate</li>
      </ul>
    </li>
    <li>Parent cycles through an array of signals, sending one to the child every second in a loop.</li>
    <li>Demonstrates bidirectional signaling, signal handling, and safe process termination.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Header</th><th>Description</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;signal.h&gt;</code></td><td>Signal handling</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;unistd.h&gt;</code></td><td>Process control and fork</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;stdio.h&gt;</code></td><td>Input/output</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>Memory allocation, exit</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>fork()</code></td><td>Create child process</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>signal()</code></td><td>Install signal handlers in parent and child</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>kill()</code></td><td>Send signal to a process</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>pause()</code></td><td>Child waits for signals</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>malloc()/free()</code></td><td>Allocate/free memory for signal array</td><td><a href="https://en.cppreference.com/w/c/memory/malloc" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>👨‍👦 Parent-child process communication</li>
    <li>🔁 Bidirectional signaling</li>
    <li>⏳ Synchronization using signals and pause()</li>
    <li>⚡ Dynamic reaction to signal events</li>
    <li>🛡️ Safe process termination via SIGINT</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li>📘 <strong>fork() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>signal() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></li>
    <li>📘 <strong>kill() man page:</strong> <a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></li>
  </ul>

</section>


<br>


<a id="c-unix-std-signal-fork-pause"></a>
<section id="c-unix-std-signal-fork-pause">

  <h2>🧪 C-Unix-STD-Signal-Fork-Pause</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal-Fork-Pause/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal-Fork-Pause/main.c"
       target="_blank"
       style="display:inline-block;padding:6px 14px;border-radius:6px;background:#24292f;color:white;text-decoration:none;font-weight:600;font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    Demonstrates <strong>parent-child synchronization using signals and pause()</strong>
    with file I/O from child processes.
  </p>
  <p>The goal is to understand:</p>
  <ul>
    <li>forking multiple child processes</li>
    <li>sending signals to children to trigger specific actions</li>
    <li>reading files in child processes and writing to stdout</li>
    <li>using pause() for waiting on signals</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Open two files for reading: <code>son1.txt</code> and <code>son2.txt</code>.</li>
    <li>Install a signal handler for <code>SIGUSR1</code> and <code>SIGCHLD</code>.</li>
    <li>Fork the first child:
      <ul>
        <li>Child pauses until <code>SIGUSR1</code> is received</li>
        <li>Reads 50 bytes from <code>son1.txt</code> and writes to stdout</li>
      </ul>
    </li>
    <li>Fork the second child:
      <ul>
        <li>Child pauses until <code>SIGUSR1</code> is received</li>
        <li>Reads 50 bytes from <code>son2.txt</code> and writes to stdout</li>
        <li>Child sleeps 5 seconds then exits</li>
      </ul>
    </li>
    <li>Parent prints PIDs of both children, sends <code>SIGUSR1</code> to each child in sequence, using pause() to synchronize.</li>
    <li>After both children finish, parent closes file descriptors and exits.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead><tr><th>Header</th><th>Description</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>&lt;signal.h&gt;</td><td>Signal handling</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;unistd.h&gt;</td><td>Process control, fork, pause</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;fcntl.h&gt;</td><td>File I/O open/read/write</td><td><a href="https://man7.org/linux/man-pages/man2/open.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;stdio.h&gt;</td><td>Standard input/output</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td>&lt;stdlib.h&gt;</td><td>Exit, malloc</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead><tr><th>Function</th><th>Role</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>fork()</td><td>Create child processes</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>signal()</td><td>Install signal handlers</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>pause()</td><td>Wait for a signal</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>open(), read(), write()</td><td>File I/O in child processes</td><td><a href="https://man7.org/linux/man-pages/man2/open.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>kill()</td><td>Send signal to child</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>👨‍👦 Parent-child communication via signals</li>
    <li>⏳ Process synchronization using pause()</li>
    <li>📂 File reading in forked processes</li>
    <li>⚡ Signal-triggered execution in children</li>
    <li>🛡️ Handling child termination signals</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">fork() man page</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">signal() man page</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">pause() man page</a></li>
  </ul>

</section>


<br>


<a id="c-unix-std-signal-fork-pause-kill"></a>
<section id="c-unix-std-signal-fork-pause-kill">

  <h2>🧪 C-Unix-STD-Signal-Fork-Pause-Kill</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal-Fork-Pause-Kill/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal-Fork-Pause-Kill/main.c"
       target="_blank"
       style="display:inline-block;padding:6px 14px;border-radius:6px;background:#24292f;color:white;text-decoration:none;font-weight:600;font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    Demonstrates <strong>signal handling and inter-process notification</strong> using
    a single child process.
  </p>
  <ul>
    <li>Child waits for <code>SIGINT</code> signal before executing</li>
    <li>Parent can send <code>SIGINT</code> to terminate the child</li>
    <li>Shows basic pause-and-signal synchronization</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Install empty signal handlers for <code>SIGINT</code> and <code>SIGCHLD</code>.</li>
    <li>Fork a child process:
      <ul>
        <li>Child pauses until <code>SIGINT</code> is received</li>
        <li>After signal, child prints a message and exits</li>
      </ul>
    </li>
    <li>Parent pauses, sends <code>SIGINT</code> to child, and waits for completion.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead><tr><th>Header</th><th>Description</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>&lt;signal.h&gt;</td><td>Signal handling</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;unistd.h&gt;</td><td>Process control</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;stdlib.h&gt;</td><td>Exit, memory allocation</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td>&lt;stdio.h&gt;</td><td>Standard I/O</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td>&lt;assert.h&gt;</td><td>Assertions for error checking</td><td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead><tr><th>Function</th><th>Role</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>fork()</td><td>Create child process</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>signal()</td><td>Install signal handlers</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>pause()</td><td>Wait for a signal</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>kill()</td><td>Send signal to child</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>👨‍👦 Parent-child synchronization via signals</li>
    <li>⏳ Using pause() for waiting signals</li>
    <li>⚡ Sending SIGINT to terminate child process</li>
    <li>🛡️ Signal handling to control execution flow</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">kill() man page</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">pause() man page</a></li>
  </ul>

</section>


<br>

<a id="c-unix-std-signal-fork-pause-kill-file-wait"></a>
<section id="c-unix-std-signal-fork-pause-kill-file-wait">

  <h2>🧪 C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait/main.c"
       target="_blank"
       style="display:inline-block;padding:6px 14px;border-radius:6px;background:#24292f;color:white;text-decoration:none;font-weight:600;font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    Demonstrates <strong>two-child process coordination using signals, pause(), and file I/O</strong>.
  </p>
  <ul>
    <li>Child processes read separate text files and print to stdout</li>
    <li>Synchronization between children using signals</li>
    <li>Parent controls execution flow</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Install signal handlers for <code>SIGUSR1</code> and <code>SIGCHLD</code>.</li>
    <li>Fork first child:
      <ul>
        <li>Wait for signal from parent</li>
        <li>Read <code>testo_1.txt</code> and print content</li>
        <li>Send signal to second child after finishing</li>
      </ul>
    </li>
    <li>Fork second child:
      <ul>
        <li>Wait for signal from first child</li>
        <li>Read <code>testo_3.txt</code> and print content</li>
        <li>Send signal back to first child or exit</li>
      </ul>
    </li>
    <li>Parent triggers first signal, then waits for both children to finish.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead><tr><th>Header</th><th>Description</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>&lt;signal.h&gt;</td><td>Signal handling</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;unistd.h&gt;</td><td>fork, pause</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;fcntl.h&gt;</td><td>File open/read</td><td><a href="https://man7.org/linux/man-pages/man2/open.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>&lt;stdio.h&gt;</td><td>File I/O and stdout</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td>&lt;stdlib.h&gt;</td><td>Exit, malloc</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td>&lt;assert.h&gt;</td><td>Error checking</td><td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead><tr><th>Function</th><th>Role</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>fork()</td><td>Create child processes</td><td><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>signal()</td><td>Install handlers for inter-process signaling</td><td><a href="https://man7.org/linux/man-pages/man2/signal.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>pause()</td><td>Wait for signals</td><td><a href="https://man7.org/linux/man-pages/man2/pause.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>open(), read(), write()</td><td>File I/O for children</td><td><a href="https://man7.org/linux/man-pages/man2/open.2.html" target="_blank">man7.org</a></td></tr>
      <tr><td>kill()</td><td>Send signals between children</td><td><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">man7.org</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>👨‍👦 Signal-based synchronization between sibling processes</li>
    <li>📂 Coordinated file reading and stdout output</li>
    <li>⏳ Using pause() for controlled execution flow</li>
    <li>⚡ Signal-triggered child-to-child communication</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li><a href="https://man7.org/linux/man-pages/man2/kill.2.html" target="_blank">kill() man page</a></li>
    <li><a href="https://man7.org/linux/man-pages/man2/fork.2.html" target="_blank">fork() man page</a></li>
  </ul>

</section>


<br>


<a id="c-unix-std-threads"></a>
<section id="c-unix-std-threads">

  <h2>🧪 C-Unix-STD-Threads</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Threads/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Threads/main.c"
       target="_blank"
       style="display:inline-block;padding:6px 14px;border-radius:6px;background:#24292f;color:white;text-decoration:none;font-weight:600;font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>creating multiple threads to process pairs of files concurrently</strong>. Each thread reads integers from an input file, sorts them, and writes to an output file.
  </p>
  <p>The goals are to understand:</p>
  <ul>
    <li>Thread creation, argument passing, and termination using <code>pthread_create</code> and <code>pthread_join</code></li>
    <li>How to process independent data concurrently</li>
    <li>Memory management for thread arguments</li>
    <li>Sorting algorithms in a multithreaded environment</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Parse command-line arguments as <code>input_file output_file</code> pairs.</li>
    <li>Allocate memory for thread IDs and thread argument structures.</li>
    <li>Create one thread per file pair, passing a structure containing input/output filenames.</li>
    <li>Each thread executes the following steps:
      <ul>
        <li>Opens the input file and reads integers into a buffer.</li>
        <li>Sorts the integers using bubble sort.</li>
        <li>Writes the sorted integers to the output file.</li>
      </ul>
    </li>
    <li>The main thread waits for the last created thread using <code>pthread_join</code> to ensure completion.</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Header</th><th>Description</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;pthread.h&gt;</code></td><td>POSIX threads API</td><td><a href="https://man7.org/linux/man-pages/man3/pthread_create.3.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;stdio.h&gt;</code></td><td>File I/O and stdout</td><td><a href="https://en.cppreference.com/w/c/io/fprintf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>Memory allocation, exit</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;string.h&gt;</code></td><td>String operations (strcpy, strlen)</td><td><a href="https://en.cppreference.com/w/c/string/byte/strcpy" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>pthread_create()</code></td><td>Create a new thread</td><td><a href="https://man7.org/linux/man-pages/man3/pthread_create.3.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>pthread_join()</code></td><td>Wait for a thread to terminate</td><td><a href="https://man7.org/linux/man-pages/man3/pthread_join.3.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>fopen()</code>, <code>fscanf()</code>, <code>fprintf()</code></td><td>File read/write operations</td><td><a href="https://en.cppreference.com/w/c/io/fscanf" target="_blank">cppreference</a></td></tr>
      <tr><td>Memory allocation (malloc/free)</td><td>Allocate memory for thread arguments and buffers</td><td><a href="https://en.cppreference.com/w/c/memory/malloc" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>⚡ Concurrent execution using threads</li>
    <li>📁 File I/O in multithreaded applications</li>
    <li>🧮 Sorting algorithms executed in parallel</li>
    <li>💾 Dynamic memory allocation for passing arguments safely to threads</li>
    <li>🔄 Synchronization by joining threads to ensure completion</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li><a href="https://man7.org/linux/man-pages/man3/pthread_create.3.html" target="_blank">POSIX pthread_create()</a></li>
    <li><a href="https://man7.org/linux/man-pages/man3/pthread_join.3.html" target="_blank">POSIX pthread_join()</a></li>
  </ul>

</section>

<br>

<a id="c-unix-std-threads-files-assert"></a>
<section id="c-unix-std-threads-files-assert">

  <h2>🧪 C-Unix-STD-Threads-Files-Assert</h2>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <p style="margin:0;">
      <strong>Path:</strong> <code>src/C-Unix-STD-Threads-Files-Assert/main.c</code>
    </p>
    <a href="https://github.com/<username>/<repo>/blob/main/src/C-Unix-STD-Threads-Files-Assert/main.c"
       target="_blank"
       style="display:inline-block;padding:6px 14px;border-radius:6px;background:#24292f;color:white;text-decoration:none;font-weight:600;font-size:0.9em;">
      🔍 View Code
    </a>
  </div>

  <h3>🎯 Purpose</h3>
  <p>
    This example demonstrates <strong>multithreaded file processing with bubble sort</strong>, using <code>assert()</code> to guarantee correctness of read/write operations.
  </p>
  <p>The goals are to understand:</p>
  <ul>
    <li>Thread-safe processing of multiple input/output files concurrently</li>
    <li>Using assertions to ensure correct file read/write</li>
    <li>Implementing bubble sort algorithm inside threads</li>
  </ul>

  <h3>🛠️ Description</h3>
  <ol>
    <li>Validate command-line arguments as <code>input_file output_file</code> pairs (odd number of arguments, at least 3).</li>
    <li>Allocate structures and thread IDs for all file pairs.</li>
    <li>Create one thread per file pair:
      <ul>
        <li>Thread reads integers from input file.</li>
        <li>Thread sorts integers using bubble sort.</li>
        <li>Thread writes sorted integers to output file.</li>
        <li>Assertions (<code>assert()</code>) verify that bytes read equal bytes written.</li>
      </ul>
    </li>
    <li>Main thread waits for the last thread to finish (<code>pthread_join</code>).</li>
  </ol>

  <h3>📦 Headers and Libraries Used</h3>
  <table>
    <thead>
      <tr><th>Header</th><th>Description</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>&lt;pthread.h&gt;</code></td><td>POSIX threads API</td><td><a href="https://man7.org/linux/man-pages/man3/pthread_create.3.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>&lt;stdio.h&gt;</code></td><td>File I/O</td><td><a href="https://en.cppreference.com/w/c/io/fscanf" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;stdlib.h&gt;</code></td><td>Memory allocation, exit</td><td><a href="https://en.cppreference.com/w/c/header/stdlib" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;assert.h&gt;</code></td><td>Error checking</td><td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td></tr>
      <tr><td><code>&lt;string.h&gt;</code></td><td>String operations</td><td><a href="https://en.cppreference.com/w/c/string/byte/strcpy" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>⚙️ System Calls and Functions</h3>
  <table>
    <thead>
      <tr><th>Function</th><th>Role</th><th>Reference</th></tr>
    </thead>
    <tbody>
      <tr><td><code>pthread_create()</code></td><td>Create thread for each file pair</td><td><a href="https://man7.org/linux/man-pages/man3/pthread_create.3.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>pthread_join()</code></td><td>Wait for threads to finish</td><td><a href="https://man7.org/linux/man-pages/man3/pthread_join.3.html" target="_blank">man7.org</a></td></tr>
      <tr><td><code>assert()</code></td><td>Verify correctness of read/write operations</td><td><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">cppreference</a></td></tr>
      <tr><td><code>fopen()/fscanf()/fprintf()/fclose()</code></td><td>File I/O operations</td><td><a href="https://en.cppreference.com/w/c/io/fscanf" target="_blank">cppreference</a></td></tr>
      <tr><td>Memory allocation (malloc/free)</td><td>Allocate thread arguments and buffers</td><td><a href="https://en.cppreference.com/w/c/memory/malloc" target="_blank">cppreference</a></td></tr>
    </tbody>
  </table>

  <h3>🧠 Key Concepts Introduced</h3>
  <ul>
    <li>⚡ Multithreading for concurrent file processing</li>
    <li>📁 Safe file I/O with assertion checks</li>
    <li>🧮 Bubble sort algorithm inside threads</li>
    <li>💾 Dynamic memory management for thread arguments</li>
    <li>🔄 Synchronization via <code>pthread_join</code> to ensure completion</li>
  </ul>

  <h3>🔗 Links</h3>
  <ul>
    <li><a href="https://man7.org/linux/man-pages/man3/pthread_create.3.html" target="_blank">POSIX pthread_create()</a></li>
    <li><a href="https://man7.org/linux/man-pages/man3/pthread_join.3.html" target="_blank">POSIX pthread_join()</a></li>
    <li><a href="https://en.cppreference.com/w/c/error/assert" target="_blank">C assert()</a></li>
  </ul>

</section>

<br>

Next step, start to use C_Linux examples by following this getting started guideline.

<br>


<a id="getting-started"></a>

# Getting Started 🚀

[Table of Contents](#table-of-contents)

This section guides you through preparing your environment and running the **C Unix & Standard Library examples** presented in this collection. The steps are tailored to Linux/Unix hosts and assume a basic familiarity with compiling and executing C programs.

- [**1 - Verify Prerequisites and Dependencies**](#prerequisites)  
  Ensure your system has the necessary **development tools** and **libraries**:  
  - **GCC or Clang** compiler (C99/C11 support)  
  - **Make** for build automation (optional but recommended)  
  - **POSIX-compliant libraries** (`<unistd.h>`, `<pthread.h>`, `<fcntl.h>`)  
  - Standard C libraries (`<stdio.h>`, `<stdlib.h>`, `<string.h>`, `<assert.h>`)  

  Reading this carefully guarantees that each example can be compiled and executed without errors.

- [**2 - Get the Source Code**](#installation)  
  Clone or download the repository containing the examples.  
  Ensure the folder structure under `<code>src/</code>` is preserved, as each example references specific file paths.

- [**3 - Build / Compile Examples**](#build)  
  Compile each example individually using GCC or your preferred compiler:  
  <code>gcc -o main main.c -lpthread</code>  
  Some examples may require the `<code>-lpthread</code>` flag for thread support. Others rely on standard POSIX calls and do not require additional flags.

- [**4 - Run Examples**](#run)  
  Execute each compiled binary from the command line.  
  - Examples using **fork(), exec(), or signals** should be run in a terminal on a Unix-like system.  
  - File-based examples require input/output files to be placed in the expected paths (`<code>src/C-STD-File/file1.txt</code>`, etc.).  
  - Threaded examples may generate multiple output files concurrently; ensure write permissions in the folder.

- [**5 - Explore and Modify**](#configuration)  
  Feel free to adjust input files, function parameters, or the number of threads in examples to experiment and observe behavior. This is ideal for learning **Unix process management**, **signals**, and **concurrent programming** in C.

- [**6 - Clean Up / Uninstall**](#uninstall)  
  Remove compiled binaries and temporary files safely:  
  <code>rm -f src/**/main</code>  
  <code>rm -f src/**/file*.out</code>  
  This ensures your workspace remains clean while preserving the original source files.

---

<p>
Following these steps guarantees that you can successfully compile, run, and experiment with all examples, from **function pointers** and **file I/O** to **Unix processes**, **signals**, and **threaded programs**.
</p>


<br>
<br>

<a id="prerequisites"></a>

## 💻 Prerequisites

Before building or running the project, make sure you satisgy the prerequisites to run the project:

- **Operating System**: GNU/Linux, Windows
- **Software Dependencies**: GitHub, Doxygen, GNU Make, GNU C Compiler

<br>
<br>

## 📦 Dependencies

Before building and generating documentation with **C_Linux**, make sure the following dependencies are installed on your system:

- **[GitHub](#install-github)** — *Optional.*  
  Even if you don’t have a GitHub account or Git installed, you can still generate documentation locally.  
  However, having a **GitHub account** and using **Git** is **recommended** for project deployment and version control.

- **[Doxygen](#install-doxygen)** — *Mandatory.*  
  Used to generate documentation from source code and Markdown files.  
  The project won’t build documentation without it.

- **[GNU Make](#install-gnu-make)** — *Mandatory.*  
  Required to run automated build and documentation generation tasks.  
  Used in this project to simplify commands such as:
  <pre>make doc</pre>
  and  
  <pre>make clean</pre>

- **[GNU C Compiler (GCC)](#install-gcc)** — *Mandatory.*  
  Required to compile all C examples in **C_Linux**.  
  Supports C99 standard and POSIX APIs.

<br>
<br>

<a id="install-github"></a>

<h2><img src="Images/Logo/GitHubLogo.svg" alt="GitHub" width="64px" height="64px"/> Install GitHub / Git </h2>

### 🐧 On GNU/Linux

<pre>
sudo apt update
sudo apt install git
</pre>

After installation, verify that Git is available:

<pre>
git --version
</pre>

To link your project to **GitHub**, create a free account at:  
👉 [https://github.com/signup](https://github.com/signup)

Then configure Git with your account details:

<pre>
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
</pre>

<br>
<br>


<h3><img src="Images/Logo/windows-svgrepo-com.svg" alt="Windows logo" width="24"/> On Windows </h3>



1. Download **Git for Windows** from:  
   👉 [https://git-scm.com/download/win](https://git-scm.com/download/win)

2. Run the installer and follow the setup wizard (leave default options checked).  
3. After installation, open **Git Bash** and verify:
   <pre>
   git --version
   </pre>

4. Optionally create a GitHub account at  
   👉 [https://github.com/signup](https://github.com/signup)

<br>
<br>

<a id="install-doxygen"></a>

<h2><img src="Images/Logo/doxygen.svg" alt="Doxygen" width="64px" height="64px"/> Install Doxygen </h2>

### 🐧 On GNU/Linux

<pre>
sudo apt update
sudo apt install doxygen graphviz
</pre>

Verify the installation:

<pre>
doxygen --version
</pre>

Optionally, you can generate a sample configuration file with:

<pre>
doxygen -g
</pre>

<br>
<br>


<h3><img src="Images/Logo/windows-svgrepo-com.svg" alt="Windows logo" width="24"/> On Windows </h3>

1. Download the Windows installer from:  
   👉 [https://www.doxygen.nl/download.html](https://www.doxygen.nl/download.html)

2. Run the `.exe` file and follow the setup wizard.  
3. After installation, open **Command Prompt** and check:
   <pre>
   doxygen --version
   </pre>

4. To enable UML and graphs, install **Graphviz** as well:  
   👉 [https://graphviz.org/download/](https://graphviz.org/download/)

<br>
<br>

<a id="install-gnu-make"></a>

<h2><img src="Images/Logo/GnuLinuxLogo.svg" alt="GNU/Linux" width="64px" height="64px"/> Install GNU Make </h2>

### 🐧 On GNU/Linux

GNU Make is usually preinstalled. Check it with:

<pre>
make --version
</pre>

If missing, install it via:

<pre>
sudo apt update
sudo apt install make
</pre>

<br>
<br>

<h3><img src="Images/Logo/windows-svgrepo-com.svg" alt="Windows logo" width="24"/> On Windows </h3>

You can install **GNU Make** in one of these ways:

#### ✅ Option 1: Using MinGW

1. Download and install **MinGW** from:  
   👉 [https://www.mingw-w64.org/](https://www.mingw-w64.org/)
2. During installation, select the “mingw32-make” package.
3. Add MinGW’s `bin` directory to your system PATH.
4. Verify installation:
   <pre>
   mingw32-make --version
   </pre>

You can then rename or alias it to `make` for convenience.

#### ✅ Option 2: Using Chocolatey (recommended if available)

If you have **Chocolatey** package manager installed:

<pre>
choco install make
</pre>

<br>
<br>

<a id="install-gcc"></a>

<h2><img src="Images/Logo/GnuLinuxLogo.svg" alt="GCC" width="64px" height="64px"/> Install GNU C Compiler (GCC)</h2>

### 🐧 On GNU/Linux

Check if GCC is already installed:

<pre>
gcc --version
</pre>

If missing, install it via:

<pre>
sudo apt update
sudo apt install gcc build-essential
</pre>

Verify installation:

<pre>
gcc --version
</pre>

---

<h3><img src="Images/Logo/windows-svgrepo-com.svg" alt="Windows logo" width="24"/> On Windows</h3>

#### ✅ Option 1: Using MinGW

1. Download and install **MinGW-w64** from:  
   👉 [https://www.mingw-w64.org/](https://www.mingw-w64.org/)  
2. During installation, select the **gcc** package.  
3. Add the `bin` directory of MinGW to your system PATH.  
4. Verify installation:

<pre>
gcc --version
</pre>

#### ✅ Option 2: Using Windows Subsystem for Linux (WSL)

1. Install WSL with a Linux distribution, e.g., Ubuntu.  
2. Open WSL terminal and run:

<pre>
sudo apt update
sudo apt install gcc build-essential
gcc --version
</pre>

#### ✅ Option 3: Using Chocolatey

If you have **Chocolatey** installed:

<pre>
choco install mingw
</pre>

Verify installation:

<pre>
gcc --version
</pre>

---

### 💡 Dependencies Verification

After installing all dependencies, verify them with:

<pre>
git --version
doxygen --version
make --version
gcc --version
</pre>

If all commands return valid version numbers, you’re ready to build and document your project 🎉

> 💡 Tip: You can also run the `doxygen.sh` script from the root directory.  
> It will automatically:
> - Check that Doxygen is installed. If not, the script will fail ❌  
> - Generate a base `Doxyfile` if missing  
> - Apply the custom configuration for **C_Linux**

<br>
<br>

<a id="installation"></a>


## ⭐ Installation

To ***install*** the project follow this setps:

A. You can download the repository from GitHub:
  ⬇️ [https://github.com/Unix69/README-Template/archive/refs/heads/main.zip](https://github.com/Unix69/README-Template/archive/refs/heads/main.zip)

  manually or by **opening a terminal** into your project destination directory, and running the following commands:

  <pre>
  mkdir project-root #create the project root directory
  cd project-root #change to the project root directory
  wget https://github.com/Unix69/C_Linux/archive/refs/heads/master.zip #make an http get request to get the project repository ** zip file ** 
  unzip master.zip #unzip the project master.zip file
  cp -R master/ ./ #copy all files recursively from the unziped master directory to your project root directory
  rm -rf master master.zip #remove the unziped master directory and master.zip file
  </pre> 

B. You can **clone the repository** from GitHub if you have Git installed by running the following commands:

  <pre>
  mkdir project-root #create the project root directory
  cd project-root #change to the project root directory
  clone https://github.com/Unix69/C_Linux.git #clone the project repository 
  cp -R C_Linux/ ./ #copy all files recursively from the C_Linux directory to your project root directory
  rm -rf C_Linux #remove the C_Linux directory. 
  </pre> 


⬇️ [Download ZIP](https://github.com/Unix69/C_Linux/archive/refs/heads/main.zip)  
🐙 [View on GitHub](https://github.com/Unix69/C_Linux)


<br>
<br>

<a id="build"></a>

## 🛠️ Build

To <b>build C_Linux full project</b> you have to build singularly:

* the example executables you want
* the C_Linux project documentation

<br>

### 1️⃣ Build All Examples

To build the entire C Unix & Standard Library examples:

1. <b>Using GNU Make</b> 🏗️

   <pre>
   make build
   make link_all
   </pre>

   <p>
   Using <code>make build</code> and <code>make link_all</code> allows compiling and linking all C examples in <code>src/</code> automatically:
   </p>
   <ul>
     <li><code>make build</code> – compiles all <code>.c</code> files in <code>src/</code> into <code>.o</code> object files.
       <ul>
         <li>Uses <code>$(CC) $(CFLAGS) -c $< -o $@</code> to compile each source file individually.</li>
         <li>Prints a message: <code>Compiling &lt;file&gt;...</code> for each compilation.</li>
       </ul>
     </li>
     <li><code>make link_all</code> – links the object files in each subfolder of <code>src/</code> into a single executable per folder.
       <ul>
         <li>Finds all <code>.o</code> files in the folder using <code>find $@ -maxdepth 1 -name "*.o"</code>.</li>
         <li>Links them with <code>gcc $(CFLAGS) &lt;objects&gt; -o &lt;folder_name&gt;</code>.</li>
         <li>Prints a success message: <code>Executable created: &lt;folder_name&gt;</code> if linking succeeds.</li>
       </ul>
     </li>
   </ul>

2. <b>Using the GNU C Compiler directly</b> 🖥️

   <pre>
   find src/ -name "main.c" -exec sh -c 'gcc -Wall -O2 "$1" -o "$(dirname "$1")/main" -lpthread && echo "$(dirname "$1")/main created" || echo "Compilation failed for $1"' _ {} \;
   </pre>

   <p>
   This command recursively compiles all <code>main.c</code> files under <code>src/</code> into executables:
   </p>
   <ul>
     <li><code>find src/ -name "main.c"</code> – locate all <code>main.c</code> files.</li>
     <li><code>-exec sh -c '...'</code> – execute a shell command for each file.</li>
     <li><code>gcc -Wall -O2 "$1" -o "$(dirname "$1")/main" -lpthread</code> – compile with warnings, optimization, and pthread support; output in the same folder.</li>
     <li><code>&& echo "$(dirname "$1")/main created"</code> – prints success message if compilation succeeds.</li>
     <li><code>|| echo "Compilation failed for $1"</code> – prints error if compilation fails.</li>
   </ul>

<br>

### 2️⃣ Build a Single Example

If you want to <b>compile only a single example</b> (e.g., `C-Func-pointer`):

1. Navigate to the example folder:

<pre>
cd src/C-Func-pointer
</pre>

2. Compile using GCC:

<pre>
gcc -o main main.c -lpthread
</pre>

3. Run the compiled example:

<pre>
./main
</pre>

This approach is ideal for <b>testing or debugging</b> individual examples. 🔍

<br>

### 3️⃣ Build the Project Documentation

<br>

#### Generate the Doxyfile

<p>
You have multiple ways to generate the documentation resources for the C Unix & Standard Library examples. Each produces a configured <code>Doxyfile</code>.
</p>

1. <b><code>./doxygen.sh</code></b> 🛠️ (Custom Doxyfile)
   <ul>
     <li>Checks if <code>doxygen</code> is installed and exits if not.</li>
     <li>Generates a default <code>Doxyfile</code> if missing.</li>
     <li>Reads <code>doxygen.ini</code> and applies tags automatically.</li>
     <li>Adds custom aliases and ensures correct output directory.</li>
   </ul>

2. <b><code>make doc_build</code></b> 📦
   <ul>
     <li>Invokes <code>doxygen.sh</code> via Makefile rule.</li>
     <li>Prepares a fully configured <code>Doxyfile</code> automatically.</li>
   </ul>

3. <b><code>doxygen -g Doxyfile</code></b> 📝 (Standard Doxyfile)
   <ul>
     <li>Generates a default <code>Doxyfile</code> template.</li>
     <li>Useful to manually edit configuration before generating documentation.</li>
   </ul>

<p>
Summary:
</p>
<ul>
  <li>Use <code>doxygen.sh</code> or <code>make doc_build</code> for automated, customized Doxyfile.</li>
  <li>Use <code>doxygen -g Doxyfile</code> for manual template creation.</li>
</ul>

<br>

#### Generate the Project Documentation

Once Doxyfile is ready:

- <b>Doxygen</b> – run directly:

<pre>
doxygen Doxyfile
</pre>

- <b><code>make doc</code></b> – generates documentation using configured <code>Doxyfile</code>:
  <ul>
    <li>Produces HTML (and other formats if enabled) in <code>docs/html</code>.</li>
    <li>Copies optional assets (images) into output folder.</li>
  </ul>

<br>
<br>


<a id="configuration"></a>

## ⚙️ Configuration

<p>
C_Linux offers multiple levels of configuration to adapt both the compilation of examples and the generation of documentation. You can adjust settings at the file, toolchain, and build system level. ⚙️
</p>

### 1️⃣ Configure Documentation

<ul>
  <li><b>Doxygen.ini</b> – Modify this file to adjust documentation parameters globally. Example:
    <pre>
DOXY_PARAMETER = "DOXY_PARAMETER-VALUE"
    </pre>
    This affects how the <code>doxygen.sh</code> script generates the <code>Doxyfile</code>.</li>

  <li><b>Doxyfile</b> – Edit after generation for fine-grained control:
    <ul>
      <li>Set <code>OUTPUT_DIRECTORY</code> for HTML/PDF outputs.</li>
      <li>Enable/disable HTML, LaTeX, or Markdown generation.</li>
      <li>Adjust inclusion/exclusion of files and folders.</li>
      <li>Add or modify <code>ALIASES</code> for custom Doxygen tags.</li>
    </ul>
  </li>

  <li><b>doxygen.sh / make doc_build</b> – Automatically reads <code>doxygen.ini</code> and generates a fully configured <code>Doxyfile</code>. ✅</li>

  <li><b>doxygen -g Doxyfile</b> – Generate a fresh, default Doxyfile if you prefer manual editing or testing new configurations.</li>
</ul>

### 2️⃣ Configure Build System

<ul>
  <li><b>Makefile & Make targets</b> – Customize the build process:
    <ul>
      <li><code>build</code> – compiles all <code>.c</code> files to <code>.o</code> object files.</li>
      <li><code>link_all</code> – links object files into one executable per folder.</li>
      <li><code>doc_build</code> – runs <code>doxygen.sh</code> to prepare documentation.</li>
      <li><code>doc</code> – runs <code>doxygen Doxyfile</code> to generate HTML/Markdown output.</li>
      <li><code>clean</code> – removes all build artifacts and documentation output.</li>
    </ul>
  </li>

  <li><b>Compiler (GCC)</b> – Modify flags and commands in Makefile or manually:
    <ul>
      <li><code>CC = gcc</code> – change compiler.</li>
      <li><code>CFLAGS = -Wall -O2</code> – adjust warning levels, optimization, or add thread support (<code>-lpthread</code>).</li>
      <li>You can also manually compile a single example:
        <pre>
gcc -o main main.c -lpthread
        </pre>
      </li>
    </ul>
  </li>

  <li><b>Source Files</b> – Organize <code>.c</code> and <code>.h</code> files in <code>src/</code> subfolders.  
    - Each subfolder produces one executable via <code>link_all</code> or can be compiled manually.  
    - File structure directly influences build and documentation inclusion.
  </li>
</ul>

### 3️⃣ Customize Markdown Documentation

<ul>
  <li>Edit <code>.md</code> files in the project to update examples’ explanations, tables, or links.</li>
  <li>Changes are automatically included in the HTML documentation when <code>make doc</code> is run.</li>
</ul>

### 💡 Notes

<ul>
  <li>Combining configuration of <code>Doxyfile</code>, <code>Makefile</code>, compiler flags, and source layout allows complete control over both executable builds and documentation generation. 🛠️</li>
  <li>Use <code>doxygen.sh</code> for automated, consistent configuration. Manual edits are useful for testing or fine-tuning. ✨</li>
  <li>Ensure any changes to source folders or files are reflected in Makefile targets to maintain build consistency. 🔄</li>
</ul>

<div id="directory-tree-container" class="directory-tree"></div>


<br>
<br>


<a id="run"></a>

## 🚀 Run

<p>
After building the project and/or the documentation, you can run both the generated documentation and the compiled examples.
</p>

### 📄 Run Documentation

<ul>
  <li>✅ The HTML documentation is available in <code>./docs/html/</code> or the path specified by <code>OUTPUT_DIRECTORY</code> in your <code>Doxyfile</code>.</li>
  <li>You can open it in a browser:
    <pre>xdg-open ./docs/html/index.html</pre>
    <small>(Linux/Unix)</small>
  </li>
  <li>On macOS:
    <pre>open ./docs/html/index.html</pre>
  </li>
  <li>📌 <b>All documentation is also fully available on GitHub</b> as linked <code>.md</code> files. This allows:
    <ul>
      <li>Browsing examples online directly.</li>
      <li>Integration with Doxygen-generated HTML documentation via GitHub Pages or other static sites.</li>
    </ul>
  </li>
</ul>

### 🧩 Run a Single Example

<p>Using <b>C-Func-pointer</b> as an example:</p>

<ul>
  <li>Navigate to the executable folder:
    <pre>cd src/C-Func-pointer</pre>
  </li>
  <li>Run the executable:
    <pre>./main</pre>
  </li>
  <li>If compiled via <code>make build</code> / <code>make link_all</code>, the executable is in the same folder as <code>main.c</code>.</li>
</ul>

### ⚙️ Run All Examples Automatically

<p>Run all executables in <code>src/</code> with a one-liner shell command:</p>

<pre>
find src/ -mindepth 1 -type f -executable -name "main" -exec sh -c './{} || echo "Execution failed for {}"' \;
</pre>

<ul>
  <li>🔹 Searches for all <code>main</code> executables in <code>src/</code> subfolders.</li>
  <li>🔹 Executes each one sequentially.</li>
  <li>🔹 Prints an error message if execution fails for a specific example.</li>
</ul>

### 💡 Notes

<ul>
  <li>Ensure examples are built first (<code>make build</code> + <code>make link_all</code>).</li>
  <li>Replace <code>C-Func-pointer</code> with any other folder to run a different example.</li>
  <li>Documentation can be refreshed anytime with <code>make doc</code>.</li>
  <li>GitHub provides an integrated view of both Doxygen HTML pages and linked <code>.md</code> files for convenient online navigation. 🌐</li>
</ul>

<br>
<br>

<a id="uninstall"></a>

## ❌ Uninstall

<p>
To <b>uninstall</b> the C_Linux project and all generated artifacts, you can use <code>make clean</code> or manually remove files.
</p>

### 🛠️ Using GNU Make

<p>Run the <code>clean</code> target from the Makefile:</p>

<pre>
make clean
</pre>

<ul>
  <li>Automatically removes:
    <ul>
      <li>All object files (<code>*.o</code>) in <code>src/</code>.</li>
      <li>All executables in <code>src/</code> subfolders.</li>
      <li>The Doxygen documentation output directory (<code>docs/</code>).</li>
    </ul>
  </li>
  <li>Preserves source files: <code>*.c</code>, headers, <code>.md</code>, etc.</li>
</ul>

### ⚙️ Manual Uninstallation

<p>If Make is not available or you want selective removal:</p>

<pre>
# Remove object files
find src/ -name "*.o" -type f -exec rm -f {} \;

# Remove compiled executables
find src/ -mindepth 1 -type f ! -name "*.c" ! -name "*.txt" ! -name "*.h" ! -name "*.hpp" -executable -exec rm -f {} \;

# Remove generated documentation
rm -rf docs/
rm -f Doxyfile
</pre>

<ul>
  <li>🔹 Deletes all <code>*.o</code> object files.</li>
  <li>🔹 Deletes executables except source, headers, and text files.</li>
  <li>🔹 Deletes documentation directory and optionally the <code>Doxyfile</code>.</li>
</ul>

### 💡 Notes

<ul>
  <li>Using <code>make clean</code> is recommended for consistent cleanup.</li>
  <li>Manual removal is useful for selective cleanup or without Make.</li>
  <li>After cleaning, you can safely rebuild examples or regenerate documentation. 🔄</li>
</ul>

<br>
<br>


<a name="license"></a>

# Licenses 📜

[Table of Contents](#table-of-contents)

<br>


This project is licensed under the <span class="md-link" data-github="LICENSE.md" data-doxygen="md_LICENSE.html">
<a href="LICENSE.md"><b>Creative Commons Attribution 4.0 International License (CC BY 4.0)</b></a>
</span>.

You are free to use, modify, and share this template — just give proper credit to **Giuseppe Pedone**.  

© 2025 Giuseppe Pedone — <span class="md-link" data-github="https://github.com/Unix69" data-doxygen="https://github.com/Unix69">
<a href="https://github.com/Unix69"><b>GitHub: Unix69</b></a>
</span>

<br>
<br>


<a name="contributing"></a>

# Contributing 👋

Thank you for your interest in **C_Linux**!  
You can freely **download and use** the C examples. To contribute, report bugs, or suggest improvements, follow the workflow below.

<br>
<br>

## General Contribution Guidelines

- Read the [**CODE_OF_CONDUCT.md**](CODE_OF_CONDUCT.md)  
- Understand the project structure  
- Ensure required tools are installed: **GCC**, **Make**, **Doxygen**  

When contributing code:

1. Fork the repository  
2. Create a **feature branch** (`git checkout -b feature/your-feature`)  
3. Make changes and commit with clear messages (`git commit -m "Add feature X"`)  
4. Push your branch to GitHub  
5. Open a **Pull Request (PR)**  

Keep style consistent, update documentation, and run tests.

<br>
<br>

<a name="authors"></a>

# Authors 🧑‍💻

<div style="display:flex; flex-direction:column; align-items:center; gap:24px;">

<div style="display:flex; align-items:flex-start; gap:16px;">
  <img src="https://avatars.githubusercontent.com/u/111588387?v=4" alt="Unix69" style="border-radius:50%; width:80px; height:80px;">
  <div>
    <strong>Giuseppe Pedone (Unix69)</strong><br>
    <span>Roles: FO, CEO</span><br>
    <span>Contributions: `FI`, `OP`, `DE`</span><br>
    <span>Email: <a href="mailto:giuseppe.pedone.developer@gmail.com">giuseppe.pedone.developer@gmail.com</a></span><br>
    <span>Links: 
      <a href="https://github.com/Unix69"><img src="Images/Logo/GitHubLogo.svg" width="20" height="20"> GitHub</a>
    </span>
  </div>
</div>

</div>

<br>
<br>

<a name="official-links"></a>

# Official Links 🌐

- [GNU C Compiler (GCC)](https://gcc.gnu.org/) – Compiler for C projects  
- [C Programming Language](https://en.wikipedia.org/wiki/C_(programming_language)) – Language reference  
- [Linux OS](https://www.linux.org/) – Target OS for examples  
- [POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/) – Standard APIs  
- [GNU Make](https://www.gnu.org/software/make/) – Build automation  
- [Doxygen](https://www.doxygen.nl/) – Documentation generator  

<br>
<br>

<a name="faq"></a>

# FAQ ❓

**Q1: Which C standard is used?**  
A1: All examples are written in **C99**.

**Q2: Supported OS?**  
A2: **POSIX-compliant systems**, mainly Linux.

**Q3: Can I modify and redistribute examples?**  
A3: Yes! All code is under **[GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)**.

**Q4: How to compile an example?**  
A4: Use `gcc` or run `make` in project root.

**Q5: How to report a bug?**  
A5: Open a **GitHub Issue** describing the error, affected example, and steps to reproduce.

<br>
<br>

<a name="fork-project"></a>

# Forking & Pull Requests 🔀

### Fork the Project

1. Go to the main repository on GitHub  
2. Click **Fork** to create your personal copy  
3. Create a branch dedicated to your feature: `git checkout -b feature-new-functionality`  
4. Keep it synchronized with the main project

### Pull Requests (PR)

1. Ensure your branch is updated with the main branch  
2. Confirm all tests and checks pass  
3. Open a PR with:
   - Clear title (e.g., "Fix: memory leak in example")  
   - Summary of changes  
   - Related issue numbers (if any)  
4. Wait for maintainers review  
5. Apply requested changes and update PR if needed  

**PR Guidelines**

- Use concise and descriptive titles  
- Include examples or references if relevant  
- Avoid committing unrelated files  

<br>
<br>

<a name="issues"></a>

# Issues ⚠️

- Issues are for reporting bugs, requesting features, or asking questions  
- Use the **[Issue Template](ISSUE_TEMPLATE.md)** if available  
- Clearly describe:
  - Issue type: bug / feature / question  
  - Steps to reproduce  
  - Expected vs actual behavior  
  - Environment: OS, version, configuration  

All issues are tracked in the **Issues** section on GitHub.

<br>
<br>

<a name="thanks"></a>

# Thanks 🙏

Special thanks to the **Open Source Community** for providing tools and frameworks such as **GCC**, **Linux**, **GNU Make**, and **Doxygen**.  
Your work empowers projects like **C_Linux** to exist and evolve.


<br>
<br>


</div>
