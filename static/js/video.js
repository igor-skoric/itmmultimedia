(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("video-modal");
    const frame = document.getElementById("video-modal-frame");
    if (!modal || !frame) return;

    function close() {
      modal.classList.remove("is-open");
      frame.innerHTML = "";
      document.body.style.overflow = "";
    }

    document.querySelectorAll(".video-thumb").forEach((btn) => {
      btn.addEventListener("click", () => {
        const source = btn.dataset.source;
        const title = btn.dataset.title || "";

        if (source === "youtube") {
          frame.innerHTML = `<iframe src="https://www.youtube.com/embed/${btn.dataset.youtube}?autoplay=1" title="${title}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
          modal.classList.add("is-open");
          document.body.style.overflow = "hidden";
          return;
        }

        if (source === "instagram") {
          window.open(btn.dataset.instagram, "_blank", "noopener");
          return;
        }

        if (source === "local") {
          frame.innerHTML = `<video controls autoplay src="${btn.dataset.local}"></video>`;
          modal.classList.add("is-open");
          document.body.style.overflow = "hidden";
        }
      });
    });

    document.getElementById("video-modal-close")?.addEventListener("click", close);
    modal.addEventListener("click", (e) => {
      if (e.target.id === "video-modal") close();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
  });
})();
