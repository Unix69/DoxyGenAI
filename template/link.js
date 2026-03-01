document.addEventListener("DOMContentLoaded", () => {
  // Verifica se siamo dentro docs/html
  const inDocsHtml = window.location.pathname.includes("/docs/html/");

  if (inDocsHtml) {
    // Aggiorna i link nei menu-links (span.md-link)
    document.querySelectorAll(".md-link").forEach(span => {
      const a = span.querySelector("a");
      const doxygenHref = span.dataset.doxygen;
      if (a && doxygenHref) {
        a.href = doxygenHref;
      }
    });

    // Aggiorna i link nella directory-tree
    document.querySelectorAll(".directory-tree a").forEach(a => {
      const span = a.closest(".md-link");
      if (span && span.dataset.doxygen) {
        a.href = span.dataset.doxygen;
      }
    });
  }
});