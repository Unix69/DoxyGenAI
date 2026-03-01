document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("directory-tree-container");
    if (!container) return;

    // Elimina tutto il contenuto statico presente
    container.innerHTML = "";

    // Ricrea il menu dinamico
    initDirectoryTree("directory-tree-container");

    // Espandere/collassare cartelle
    container.querySelectorAll(".folder").forEach(folder => {
        folder.addEventListener("click", e => {
            e.stopPropagation();
            folder.classList.toggle("expanded");
        });
    });
});

// ======================== FUNZIONI ========================= //

function showPreview(filename, url) {
    fetch(url)
      .then(res => res.text())
      .then(content => {
          const modal = document.createElement("div");
          modal.style.position = "fixed";
          modal.style.top = "0";
          modal.style.left = "0";
          modal.style.width = "100%";
          modal.style.height = "100%";
          modal.style.backgroundColor = "rgba(0,0,0,0.7)";
          modal.style.display = "flex";
          modal.style.alignItems = "center";
          modal.style.justifyContent = "center";
          modal.style.zIndex = "10000";

          const box = document.createElement("pre");
          box.style.background = "#fff";
          box.style.color = "#000";
          box.style.padding = "20px";
          box.style.maxWidth = "90%";
          box.style.maxHeight = "90%";
          box.style.overflow = "auto";
          box.textContent = content;

          modal.addEventListener("click", () => modal.remove());
          box.addEventListener("click", e => e.stopPropagation());

          modal.appendChild(box);
          document.body.appendChild(modal);
      })
      .catch(err => alert("Impossibile caricare il file: " + filename));
}

function initDirectoryTree(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    let basePath = "";
    if (window.location.pathname.includes("/docs/html")) {
        basePath = "../../";
    }

    const treeData = [
        { type: "file", name: "README.md", icon: "📝", link: basePath + "docs/html/md_README.html" },
        { type: "file", name: "ISSUE_TEMPLATE.md", icon: "📝", link: basePath + "docs/html/md_ISSUE_TEMPLATE.html" },
        { type: "file", name: "CONTACT_US.md", icon: "☎️", link: basePath + "docs/html/md_CONTACT_US.html" },
        { type: "file", name: "template.css", icon: "🎨", link: basePath + "docs/html/template.css" },
        { type: "file", name: "LICENSE.md", icon: "📜", link: basePath + "docs/html/md_LICENSE.html" },
        { type: "file", name: "CODE_OF_CONDUCT.md", icon: "📝", link: basePath + "docs/html/md_CODE_OF_CONDUCT.html" },
        { type: "file", name: "Makefile", icon: "📄", link: basePath + "Makefile", preview: true },
        { type: "file", name: "Doxyfile", icon: "⚙️", link: basePath + "Doxyfile", preview: true },
        { type: "file", name: "doxygen.sh", icon: "🐚", link: basePath + "doxygen.sh", preview: true },
        { type: "file", name: "DoxygenLayout.xml", icon: "⚙️", link: basePath + "DoxygenLayout.xml" },
        { type: "file", name: "doxygen.ini", icon: "🐚", link: basePath + "doxygen.ini" },
        { type: "file", name: "link.js", icon: "📄", link: basePath + "link.js" },
        { type: "file", name: "directory-tree.js", icon: "🐚", link: basePath + "directory-tree.js" },
        { type: "file", name: "header.html", icon: "📄", link: basePath + "header.html", preview: true },
        { type: "file", name: "footer.html", icon: "📄", link: basePath + "footer.html", preview: true },
        { type: "file", name: "index.html", icon: "📄", link: basePath + "index.html", preview: true },
        {type:"folder", name:"src", icon:"📁",
            children:[

                { type:"folder", name:"C-Func-pointer",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Func-pointer/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-STD-File",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-STD-File/main.c", preview:true },
                    { type:"file", name:"file1.txt", link:basePath+"src/C-STD-File/file1.txt", preview:true },
                    { type:"file", name:"file2.txt", link:basePath+"src/C-STD-File/file2.txt", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Basic-Fork",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Basic-Fork/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Copy-DirectoryTree",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Copy-DirectoryTree/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Execl",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Execl/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Execlp-System",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Execlp-System/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Explore-File-Directories",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Explore-File-Directories/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Fork",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Fork/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Fork-Sleep",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Fork-Sleep/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Fork-Wait",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Fork-Wait/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Fork-WaitPid",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Fork-WaitPid/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Fork-Wait-Precedence",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Fork-Wait-Precedence/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Kill",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Kill/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Signal",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Signal-Fork",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal-Fork/main.c", preview:true }
                ]
                },

                { type:"folder", name:"C-Unix-STD-Signal-Fork-Kill",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal-Fork-Kill/main.c", preview:true }
                ]
                },
                { type:"folder", name:"C-Unix-STD-Signal-Fork-Pause",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause/main.c", preview:true },
                    { type:"file", name:"son1.txt", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause/son1.txt", preview:true },
                    { type:"file", name:"son2.txt", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause/son2.txt", preview:true }
                ]
                },
                { type:"folder", name:"C-Unix-STD-Signal-Fork-Pause-Kill",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause-Kill/main.c", preview:true }
                ]
                },
                { type:"folder", name:"C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait/main.c", preview:true },
                    { type:"file", name:"testo_1.txt", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait/testo_1.txt", preview:true },
                    { type:"file", name:"testo_3.txt", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause-Kill-File-Wait/testo_3.txt", preview:true }
                ]
                },
                { type:"folder", name:"C-Unix-STD-Signal-Fork-Pause-Kill-Pipe",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause-Kill-Pipe/main.c", preview:true },
                    { type:"file", name:"testo.txt", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause-Kill-Pipe/testo.txt", preview:true }
                ]
                },
                { type:"folder", name:"C-Unix-STD-Signal-Fork-Pause-Kill-Wait",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Signal-Fork-Pause-Kill-Wait/main.c", preview:true }
                ]
                },
                { type:"folder", name:"C-Unix-STD-Threads",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Threads/main.c", preview:true }
                ]
                },
                { type:"folder", name:"C-Unix-STD-Threads-Files-Assert",
                children:[
                    { type:"file", name:"main.c", link:basePath+"src/C-Unix-STD-Threads-Files-Assert/main.c", preview:true },
                    { type:"file", name:"file1in.txt", link:basePath+"src/C-Unix-STD-Threads-Files-Assert/file1in.txt", preview:true },
                    { type:"file", name:"file1out.txt", link:basePath+"src/C-Unix-STD-Threads-Files-Assert/file1out.txt", preview:true },
                    { type:"file", name:"file2in.txt", link:basePath+"src/C-Unix-STD-Threads-Files-Assert/file2in.txt", preview:true },
                    { type:"file", name:"file2out.txt", link:basePath+"src/C-Unix-STD-Threads-Files-Assert/file2out.txt", preview:true },
                    { type:"file", name:"file3in.txt", link:basePath+"src/C-Unix-STD-Threads-Files-Assert/file3in.txt", preview:true },
                    { type:"file", name:"file3out.txt", link:basePath+"src/C-Unix-STD-Threads-Files-Assert/file3out.txt", preview:true }
                ]
        }]}
    ];

    function createTree(data) {
        const ul = document.createElement("ul");

        data.forEach(item => {
            const li = document.createElement("li");
            li.className = item.type;

            const icon = item.icon ?? (item.type === "folder" ? "📁" : "📄");
            li.appendChild(document.createTextNode(icon + " "));

            if (item.type === "folder") {
                li.appendChild(document.createTextNode(item.name));
                if (item.children?.length) {
                    li.appendChild(createTree(item.children));
                }
            }

            if (item.type === "file") {
                const a = document.createElement("a");
                a.textContent = item.name;
                a.href = item.link || "#";

                if (item.preview) {
                    a.addEventListener("click", e => {
                        e.preventDefault();
                        showPreview(item.name, item.link);
                    });
                }

                li.appendChild(a);
            }

            ul.appendChild(li);
        });

        return ul;
    }

    container.appendChild(createTree(treeData));
}