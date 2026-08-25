(function () {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const boot = document.getElementById("boot");
  const bootTc = boot?.querySelector("[data-boot-tc]");
  let bootDone = false;
  let heroStarted = false;
  let bootFrames = 0;
  let bootRaf = 0;

  const bootStarted = performance.now();
  const bootMinMs = 2400;

  const tickBoot = () => {
    if (bootDone) return;
    bootFrames += 1;
    if (bootTc) {
      const f = bootFrames % 24;
      const s = Math.floor(bootFrames / 24) % 60;
      bootTc.textContent =
        "00:00:" + String(s).padStart(2, "0") + ":" + String(f).padStart(2, "0");
    }
    bootRaf = requestAnimationFrame(tickBoot);
  };

  if (boot && !reduceMotion) {
    bootRaf = requestAnimationFrame(tickBoot);
  }

  const finishBoot = () => {
    if (bootDone) return;
    bootDone = true;
    if (bootRaf) cancelAnimationFrame(bootRaf);
    document.documentElement.classList.remove("is-booting");
    document.body.classList.remove("is-booting");
    if (!boot) {
      window.dispatchEvent(new Event("itm:ready"));
      return;
    }
    if (reduceMotion) {
      boot.remove();
      window.dispatchEvent(new Event("itm:ready"));
      return;
    }
    boot.classList.add("is-done");
    let released = false;
    const after = () => {
      if (released) return;
      released = true;
      boot.remove();
      window.dispatchEvent(new Event("itm:ready"));
    };
    boot.addEventListener("transitionend", after, { once: true });
    setTimeout(after, 650);
  };

  const releaseBoot = () => {
    const wait = Math.max(0, bootMinMs - (performance.now() - bootStarted));
    setTimeout(finishBoot, reduceMotion ? 0 : wait);
  };

  if (!boot) {
    finishBoot();
  } else if (document.readyState === "complete") {
    releaseBoot();
  } else {
    window.addEventListener("load", releaseBoot, { once: true });
    setTimeout(releaseBoot, 6500);
  }

  document.addEventListener("DOMContentLoaded", () => {
    const header = document.getElementById("site-header");
    const toggle = document.getElementById("menu-toggle");
    const panel = document.getElementById("nav-panel");
    const mobile = window.matchMedia("(max-width: 720px)").matches;

    let compact = window.scrollY > 24;
    const setCompact = (on) => {
      compact = on;
      header?.classList.toggle("is-scrolled", on);
      document.documentElement.classList.toggle("is-scrolled", on);
    };
    const camFab = document.getElementById("cam-fab");
    const hero = document.querySelector(".hero");
    const updateCamFab = () => {
      if (!camFab) return;
      const threshold = hero ? Math.max(hero.offsetHeight * 0.55, 380) : 240;
      camFab.classList.toggle("is-on", window.scrollY > threshold && !camFab.classList.contains("is-rising"));
    };
    const onScroll = () => {
      const y = window.scrollY;
      if (!compact && y > 36) setCompact(true);
      else if (compact && y < 10) setCompact(false);
      updateCamFab();
    };
    setCompact(compact);
    window.addEventListener("scroll", onScroll, { passive: true });

    const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
    let camScrollRaf = 0;
    const goToTop = (smooth) => {
      if (camScrollRaf) cancelAnimationFrame(camScrollRaf);
      const start = window.scrollY;
      if (!smooth || start <= 1) {
        window.scrollTo(0, 0);
        return Promise.resolve();
      }
      const duration = Math.min(1600, Math.max(1000, start * 0.48));
      const t0 = performance.now();
      return new Promise((resolve) => {
        const step = (now) => {
          const t = Math.min(1, (now - t0) / duration);
          window.scrollTo(0, Math.round(start * (1 - easeInOut(t))));
          if (t < 1) camScrollRaf = requestAnimationFrame(step);
          else {
            camScrollRaf = 0;
            window.scrollTo(0, 0);
            resolve();
          }
        };
        camScrollRaf = requestAnimationFrame(step);
      });
    };
    camFab?.addEventListener("click", () => {
      if (camFab.classList.contains("is-rising")) return;
      if (reduceMotion) {
        goToTop(false);
        updateCamFab();
        return;
      }
      const duration = Math.min(1600, Math.max(1000, window.scrollY * 0.48));
      camFab.style.animationDuration = `${duration}ms`;
      camFab.classList.add("is-rising");
      camFab.classList.remove("is-on");
      goToTop(true).then(() => {
        camFab.classList.remove("is-rising");
        camFab.style.animationDuration = "";
        updateCamFab();
      });
    });
    if (bootDone) updateCamFab();
    else window.addEventListener("itm:ready", updateCamFab, { once: true });

    const setMenu = (open) => {
      panel?.classList.toggle("is-open", open);
      toggle?.setAttribute("aria-expanded", open ? "true" : "false");
      document.documentElement.classList.toggle("is-nav-open", open);
      document.body.classList.toggle("is-nav-open", open);
    };

    toggle?.addEventListener("click", () => {
      setMenu(!panel?.classList.contains("is-open"));
    });

    panel?.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setMenu(false));
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") setMenu(false);
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 1080) setMenu(false);
    });

    const nodes = document.querySelectorAll(".reveal");
    if (nodes.length) {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              io.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.08, rootMargin: "80px 0px" }
      );
      nodes.forEach((n) => io.observe(n));
    }

    document.querySelectorAll(".partners-rail").forEach((rail) => {
      const band = rail.closest(".partners-band") || rail.parentElement;
      const indexEl = band?.querySelector("[data-partners-index] b");
      const prev = band?.querySelector("[data-partners-prev]");
      const next = band?.querySelector("[data-partners-next]");
      const cards = [...rail.querySelectorAll(".partner-card")];

      const stepSize = () => {
        const card = cards[0];
        if (!card) return rail.clientWidth;
        const styles = window.getComputedStyle(rail);
        const gap = parseFloat(styles.columnGap || styles.gap) || 0;
        return card.getBoundingClientRect().width + gap;
      };

      const currentIndex = () => {
        const step = stepSize();
        if (!step) return 0;
        return Math.min(cards.length - 1, Math.max(0, Math.round(rail.scrollLeft / step)));
      };

      const sync = () => {
        const index = currentIndex();
        if (indexEl) indexEl.textContent = String(index + 1).padStart(2, "0");
        const maxLeft = Math.max(0, rail.scrollWidth - rail.clientWidth - 2);
        if (prev) prev.disabled = rail.scrollLeft <= 2;
        if (next) next.disabled = rail.scrollLeft >= maxLeft;
      };

      const go = (dir) => {
        rail.scrollBy({
          left: dir * stepSize(),
          behavior: reduceMotion ? "auto" : "smooth",
        });
      };

      prev?.addEventListener("click", () => go(-1));
      next?.addEventListener("click", () => go(1));
      rail.addEventListener("scroll", sync, { passive: true });
      window.addEventListener("resize", sync);
      sync();

      rail.addEventListener(
        "wheel",
        (event) => {
          if (rail.scrollWidth <= rail.clientWidth + 1) return;
          if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;
          const atStart = rail.scrollLeft <= 0;
          const atEnd = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 1;
          if ((event.deltaY < 0 && atStart) || (event.deltaY > 0 && atEnd)) return;
          rail.scrollLeft += event.deltaY;
          event.preventDefault();
        },
        { passive: false }
      );
    });

    document.querySelectorAll(".page-loop-video").forEach((video) => {
      if (reduceMotion) {
        video.remove();
        return;
      }
      const hd = video.dataset.srcHd;
      const sd = video.dataset.srcSd;
      if (hd || sd) {
        video.src = mobile && sd ? sd : hd || sd;
      }
      video.addEventListener("error", () => video.remove());
      video.play().catch(() => {});
    });

    const heroVideo = document.querySelector(".hero-video");
    const startHeroVideo = () => {
      if (!heroVideo || reduceMotion) return;
      const src = heroVideo.dataset.src;
      if (src && heroVideo.src !== src) heroVideo.src = src;
      const play = () => heroVideo.play().catch(() => {});
      heroVideo.addEventListener("playing", () => heroVideo.classList.add("is-ready"), { once: true });
      heroVideo.addEventListener("error", () => heroVideo.remove(), { once: true });
      play();
      if ("IntersectionObserver" in window) {
        const io = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) play();
              else heroVideo.pause();
            });
          },
          { threshold: 0.12 }
        );
        io.observe(heroVideo);
      }
    };
    if (bootDone) startHeroVideo();
    else window.addEventListener("itm:ready", startHeroVideo, { once: true });

    const startHero = () => {
      if (heroStarted) return;
      heroStarted = true;
      const typeRoot = document.querySelector("[data-typewriter]");
      const fadeNodes = document.querySelectorAll("[data-hero-fade]");
      const showFade = () => fadeNodes.forEach((el) => el.classList.add("is-in"));

      if (!typeRoot) {
        showFade();
        return;
      }

      const lines = [...typeRoot.querySelectorAll("[data-type]")];
      if (reduceMotion) {
        lines.forEach((el) => {
          el.textContent = el.dataset.type || "";
        });
        showFade();
        return;
      }

      const caret = document.createElement("span");
      caret.className = "caret";
      caret.setAttribute("aria-hidden", "true");
      let line = 0;
      const typeLine = () => {
        if (line >= lines.length) {
          caret.remove();
          showFade();
          return;
        }
        const el = lines[line];
        const text = el.dataset.type || "";
        let i = 0;
        const step = () => {
          i += 1;
          el.textContent = text.slice(0, i);
          el.appendChild(caret);
          if (i < text.length) {
            setTimeout(step, 32);
          } else {
            line += 1;
            setTimeout(typeLine, 160);
          }
        };
        step();
      };
      typeLine();
    };

    if (bootDone) startHero();
    else window.addEventListener("itm:ready", startHero, { once: true });

    const wave = document.getElementById("hero-wave");
    const glow = document.getElementById("hero-glow");
    if (hero && wave) {
      const ctx = wave.getContext("2d", { alpha: true });
      const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
      const isMobile = window.matchMedia("(max-width: 720px)").matches;
      const mouseOn = finePointer && !reduceMotion && !isMobile;
      let width = 0;
      let height = 0;
      let time = 0;
      let running = false;
      let visible = true;
      let raf = 0;
      const mouse = { x: 0, y: 0, tx: 0, ty: 0, active: 0, tActive: 0 };

      const resize = () => {
        const rect = hero.getBoundingClientRect();
        width = Math.max(1, Math.floor(rect.width));
        height = Math.max(1, Math.floor(rect.height));
        const dpr = Math.min(window.devicePixelRatio || 1, isMobile ? 1 : 1.5);
        wave.width = Math.floor(width * dpr);
        wave.height = Math.floor(height * dpr);
        wave.style.width = width + "px";
        wave.style.height = height + "px";
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      };

      const draw = (staticFrame) => {
        if (!width || !height) return;
        ctx.clearRect(0, 0, width, height);
        if (!staticFrame) time += isMobile ? 0.0038 : 0.0052;

        mouse.x += (mouse.tx - mouse.x) * 0.045;
        mouse.y += (mouse.ty - mouse.y) * 0.045;
        mouse.active += (mouse.tActive - mouse.active) * 0.06;

        if (glow && mouseOn) {
          glow.style.transform = `translate3d(${mouse.x}px, ${mouse.y}px, 0)`;
          glow.classList.toggle("is-on", mouse.active > 0.08);
        }

        const rows = isMobile ? 6 : 13;
        const cols = isMobile ? 36 : 78;
        const span = width * (isMobile ? 0.995 : 1);
        const baseY = height * (isMobile ? 0.96 : 0.93);
        const rowGap = isMobile ? 5.5 : 8;
        const amp = isMobile ? 12 : 28;
        const grid = [];

        for (let r = 0; r < rows; r++) {
          const line = [];
          const speed = 0.24 + r * 0.075;
          const twist = 0.55 + (r % 3) * 0.22;
          for (let c = 0; c < cols; c++) {
            const u = c / (cols - 1);
            const env = 0.38 + 0.62 * Math.pow(1 - u, 0.42);
            let x =
              u * span +
              Math.sin(u * 6.4 + time * speed * 0.45 + r * 0.85) * 22 * env * twist;
            let y =
              baseY -
              r * rowGap -
              Math.sin(u * 5.4 + time * speed + r * 0.72) * amp * env -
              Math.sin(u * 10.6 - time * (speed * 0.58) + r * 1.25) * amp * 0.48 * env -
              Math.cos(u * 2.35 + time * 0.26 + r * 0.48) * amp * 0.42 * env -
              Math.sin(u * 16.8 + time * 0.16 + r * 0.9) * amp * 0.2 * env;

            if (mouseOn && mouse.active > 0.02) {
              const dx = x - mouse.x;
              const dy = y - mouse.y;
              const dist = Math.sqrt(dx * dx + dy * dy);
              const radius = 210;
              if (dist < radius) {
                const f = (1 - dist / radius) ** 2 * mouse.active;
                y -= f * 20;
                x += (dx / (dist || 1)) * f * 11;
              }
            }

            line.push({ x, y, u, env });
          }
          grid.push(line);
        }

        ctx.lineJoin = "round";
        ctx.lineCap = "round";

        for (let r = 0; r < rows; r++) {
          const strength = (1 - r / rows) * 0.2 + 0.055;
          const grad = ctx.createLinearGradient(0, 0, span, 0);
          grad.addColorStop(0, `rgba(250, 88, 23, ${strength})`);
          grad.addColorStop(0.62, `rgba(250, 88, 23, ${strength * 0.82})`);
          grad.addColorStop(1, `rgba(250, 88, 23, ${strength * 0.42})`);
          ctx.beginPath();
          grid[r].forEach((p, i) => {
            if (i === 0) ctx.moveTo(p.x, p.y);
            else ctx.lineTo(p.x, p.y);
          });
          ctx.strokeStyle = grad;
          ctx.lineWidth = r === 0 ? 1.2 : 0.65;
          ctx.stroke();

          if (r < rows - 1) {
            const step = isMobile ? 3 : 2;
            for (let c = 0; c < cols; c += step) {
              const a = grid[r][c];
              const b = grid[r + 1][c];
              ctx.beginPath();
              ctx.moveTo(a.x, a.y);
              ctx.lineTo(b.x, b.y);
              ctx.strokeStyle = `rgba(250, 88, 23, ${a.env * 0.14})`;
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        }

        const sparkEvery = isMobile ? 3 : 2;
        for (let r = 0; r < rows; r++) {
          for (let c = 0; c < cols; c++) {
            const p = grid[r][c];
            const pulse = 0.62 + 0.38 * Math.sin(time * 1.15 + c * 0.31 + r * 0.8);
            const hot = 0.75 + 0.25 * Math.sin(time * 0.35 + c * 0.17);
            const alpha = p.env * (0.2 + 0.55 * pulse) * hot;
            if (alpha < 0.04) continue;

            if (c % sparkEvery === 0 || (c + r) % 4 === 0) {
              const radius = (isMobile ? 0.7 : 1.05) * (0.7 + pulse * 0.55);
              ctx.beginPath();
              ctx.arc(p.x, p.y, radius * 2.4, 0, Math.PI * 2);
              ctx.fillStyle = `rgba(250, 88, 23, ${alpha * 0.12})`;
              ctx.fill();
              ctx.beginPath();
              ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
              ctx.fillStyle = `rgba(255, 168, 120, ${Math.min(0.75, alpha)})`;
              ctx.fill();
            } else {
              ctx.beginPath();
              ctx.arc(p.x, p.y, isMobile ? 0.55 : 0.7, 0, Math.PI * 2);
              ctx.fillStyle = `rgba(250, 88, 23, ${alpha * 0.55})`;
              ctx.fill();
            }
          }
        }
      };

      const loop = () => {
        if (!running) return;
        draw(false);
        raf = requestAnimationFrame(loop);
      };

      const start = () => {
        if (running || reduceMotion) return;
        running = true;
        raf = requestAnimationFrame(loop);
      };

      const stop = () => {
        running = false;
        if (raf) cancelAnimationFrame(raf);
        raf = 0;
      };

      resize();
      draw(true);

      if (!reduceMotion) {
        const vis = new IntersectionObserver(
          (entries) => {
            visible = Boolean(entries[0]?.isIntersecting);
            if (visible) start();
            else stop();
          },
          { threshold: 0.08 }
        );
        vis.observe(hero);
        start();
      }

      window.addEventListener(
        "resize",
        () => {
          resize();
          if (reduceMotion || !running) draw(true);
        },
        { passive: true }
      );

      if (mouseOn) {
        hero.addEventListener(
          "pointermove",
          (e) => {
            if (e.pointerType && e.pointerType !== "mouse") return;
            const rect = hero.getBoundingClientRect();
            mouse.tx = e.clientX - rect.left;
            mouse.ty = e.clientY - rect.top;
            mouse.tActive = 1;
          },
          { passive: true }
        );
        hero.addEventListener(
          "pointerleave",
          () => {
            mouse.tActive = 0;
          },
          { passive: true }
        );
      }
    }

    const fx = document.getElementById("edit-fx");
    const facetShift = document.querySelector(".site-facets-shift");
    let facetY = 0;
    let facetV = 0;
    let facetTarget = 0;
    let facetRun = false;

    const stepFacets = () => {
      facetV += (facetTarget - facetY) * 0.045;
      facetV *= 0.86;
      facetY += facetV;
      if (facetShift) {
        facetShift.style.transform = `translate3d(0, ${facetY.toFixed(2)}px, 0)`;
      }
      if (Math.abs(facetTarget - facetY) > 0.2 || Math.abs(facetV) > 0.2) {
        facetRun = true;
        requestAnimationFrame(stepFacets);
      } else {
        facetRun = false;
      }
    };

    const kickFacets = () => {
      if (!facetShift || reduceMotion) return;
      const y = window.scrollY;
      facetTarget = Math.max(-72, Math.min(72, y * -0.055));
      if (!facetRun) {
        facetRun = true;
        requestAnimationFrame(stepFacets);
      }
    };

    if (fx) {
      const tc = fx.querySelector("[data-edit-tc]");
      const fill = fx.querySelector(".edit-fx-scale-fill");
      const playhead = fx.querySelector(".edit-fx-playhead");
      const scale = fx.querySelector(".edit-fx-scale");
      const hero = document.querySelector(".hero");
      let fxTick = false;
      const updateFx = () => {
        fxTick = false;
        const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
        const p = Math.min(1, Math.max(0, window.scrollY / max));
        if (fill) fill.style.transform = `scaleY(${p})`;
        if (playhead && scale) {
          playhead.style.transform = `translate3d(0, ${p * Math.max(0, scale.clientHeight - 2)}px, 0)`;
        }
        if (scale && hero) {
          const fadeEnd = Math.max(1, hero.offsetHeight * 0.72);
          const t = Math.min(1, Math.max(0, window.scrollY / fadeEnd));
          scale.style.opacity = String(t * t * (3 - 2 * t));
        } else if (scale) {
          scale.style.opacity = "1";
        }
        if (tc) {
          const frames = Math.floor(p * 96 * 24);
          const f = frames % 24;
          const s = Math.floor(frames / 24) % 60;
          const m = Math.floor(frames / 24 / 60) % 60;
          tc.textContent =
            "00:" +
            String(m).padStart(2, "0") +
            ":" +
            String(s).padStart(2, "0") +
            ":" +
            String(f).padStart(2, "0");
        }
      };
      updateFx();
      window.addEventListener(
        "scroll",
        () => {
          kickFacets();
          if (!fxTick) {
            fxTick = true;
            requestAnimationFrame(updateFx);
          }
        },
        { passive: true }
      );
    } else {
      window.addEventListener("scroll", kickFacets, { passive: true });
    }
    kickFacets();
  });
})();
