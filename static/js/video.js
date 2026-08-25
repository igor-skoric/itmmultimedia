(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("video-modal");
    const frame = document.getElementById("video-modal-frame");
    if (!modal || !frame) return;

    function close() {
      modal.classList.remove("is-open");
      frame.replaceChildren();
      document.body.style.overflow = "";
    }

    function openModal() {
      modal.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }

    document.querySelectorAll(".video-thumb").forEach((btn) => {
      btn.addEventListener("click", () => {
        const source = btn.dataset.source;
        const title = btn.dataset.title || "";

        if (source === "youtube") {
          const id = (btn.dataset.youtube || "").trim();
          if (!id) return;
          const iframe = document.createElement("iframe");
          const params = new URLSearchParams({
            autoplay: "1",
            rel: "0",
            modestbranding: "1",
            playsinline: "1",
            origin: window.location.origin,
          });
          iframe.src = "https://www.youtube-nocookie.com/embed/" + id + "?" + params.toString();
          iframe.title = title;
          iframe.allow =
            "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
          iframe.allowFullscreen = true;
          iframe.referrerPolicy = "strict-origin-when-cross-origin";
          frame.replaceChildren(iframe);
          openModal();
          return;
        }

        if (source === "instagram") {
          window.open(btn.dataset.instagram, "_blank", "noopener");
          return;
        }

        if (source === "local") {
          const video = document.createElement("video");
          video.controls = true;
          video.autoplay = true;
          video.src = btn.dataset.local || "";
          frame.replaceChildren(video);
          openModal();
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
