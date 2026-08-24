(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const items = Array.from(document.querySelectorAll(".gallery-item"));
    const modal = document.getElementById("lightbox");
    const img = document.getElementById("lightbox-image");
    const caption = document.getElementById("lightbox-caption");
    if (!items.length || !modal || !img) return;

    let index = 0;

    function open(i) {
      index = i;
      const item = items[index];
      img.src = item.dataset.full;
      img.alt = item.dataset.caption || "";
      if (caption) caption.textContent = item.dataset.caption || "";
      modal.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }

    function close() {
      modal.classList.remove("is-open");
      document.body.style.overflow = "";
    }

    function step(dir) {
      index = (index + dir + items.length) % items.length;
      open(index);
    }

    items.forEach((item, i) => item.addEventListener("click", () => open(i)));
    document.getElementById("lightbox-close")?.addEventListener("click", close);
    document.getElementById("lightbox-prev")?.addEventListener("click", () => step(-1));
    document.getElementById("lightbox-next")?.addEventListener("click", () => step(1));
    modal.addEventListener("click", (e) => {
      if (e.target.id === "lightbox") close();
    });
    document.addEventListener("keydown", (e) => {
      if (!modal.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    });
  });
})();
