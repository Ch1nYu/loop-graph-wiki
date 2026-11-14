(function () {
  "use strict";

  const slides = Array.from(document.querySelectorAll(".slide"));
  const stage = document.querySelector(".stage");
  const progressBar = document.getElementById("progressBar");
  const hudCounter = document.getElementById("hudCounter");
  const overview = document.getElementById("overview");
  const overviewGrid = document.getElementById("overviewGrid");
  const help = document.getElementById("help");
  const params = new URLSearchParams(window.location.search);
  let current = 0;

  if (params.get("qa") === "1") {
    document.documentElement.dataset.static = "true";
  }

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function fit() {
    const scale = Math.min(window.innerWidth / 1600, window.innerHeight / 900);
    document.documentElement.style.setProperty("--scale", String(scale));
  }

  function slideTitle(slide) {
    const heading = slide.querySelector("h1, h2");
    return heading ? heading.textContent.replace(/\s+/g, " ").trim() : slide.id;
  }

  function show(index, updateHash) {
    if (!slides.length) return;
    current = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === current);
      slide.setAttribute("aria-hidden", i === current ? "false" : "true");
    });
    if (progressBar) {
      progressBar.style.width = ((current + 1) / slides.length) * 100 + "%";
    }
    if (hudCounter) {
      hudCounter.textContent = pad(current + 1) + " / " + pad(slides.length);
    }
    if (updateHash !== false) {
      history.replaceState(null, "", "#slide-" + (current + 1));
    }
  }

  function next() {
    show(current + 1);
  }

  function prev() {
    show(current - 1);
  }

  function buildOverview() {
    if (!overviewGrid) return;
    overviewGrid.innerHTML = "";
    slides.forEach((slide, i) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "overview-card";
      card.innerHTML =
        '<div class="n">' + pad(i + 1) + "</div>" +
        '<div class="t">' + slideTitle(slide) + "</div>";
      card.addEventListener("click", () => {
        show(i);
        closeOverlays();
      });
      overviewGrid.appendChild(card);
    });
  }

  function openOverview() {
    if (!overview) return;
    buildOverview();
    overview.classList.add("is-open");
    overview.setAttribute("aria-hidden", "false");
  }

  function openHelp() {
    if (!help) return;
    help.classList.add("is-open");
    help.setAttribute("aria-hidden", "false");
  }

  function closeOverlays() {
    [overview, help].forEach((el) => {
      if (!el) return;
      el.classList.remove("is-open");
      el.setAttribute("aria-hidden", "true");
    });
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }

  function runQA() {
    const report = {
      slideCount: slides.length,
      overflow: [],
      missingCitations: [],
      generatedAt: new Date().toISOString(),
    };
    slides.forEach((slide, i) => {
      const inner = slide.querySelector(".slide-inner");
      if (!inner) {
        report.overflow.push({ slide: i + 1, id: slide.id, reason: "missing .slide-inner" });
        return;
      }
      const dh = inner.scrollHeight - inner.clientHeight;
      const dw = inner.scrollWidth - inner.clientWidth;
      if (dh > 1 || dw > 1) {
        report.overflow.push({
          slide: i + 1,
          id: slide.id,
          dh: dh,
          dw: dw,
          scrollH: inner.scrollHeight,
          clientH: inner.clientHeight,
          scrollW: inner.scrollWidth,
          clientW: inner.clientWidth,
        });
      }
      if (!slide.querySelector(".cite-chip")) {
        report.missingCitations.push(i + 1);
      }
    });
    report.pass = report.overflow.length === 0 && report.missingCitations.length === 0;
    const target = document.getElementById("qa-report");
    if (target) target.textContent = JSON.stringify(report);
    document.documentElement.dataset.qa = report.pass ? "pass" : "fail";
    document.documentElement.dataset.ready = "true";
  }

  function initialIndex() {
    const querySlide = Number(params.get("slide"));
    if (Number.isFinite(querySlide) && querySlide >= 1) return querySlide - 1;
    const match = window.location.hash.match(/slide-(\d+)/);
    if (match) return Number(match[1]) - 1;
    return 0;
  }

  document.addEventListener("keydown", (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const key = event.key;
    if (key === "Escape") {
      closeOverlays();
      return;
    }
    if (overview && overview.classList.contains("is-open")) {
      if (key === "ArrowRight" || key === "ArrowDown" || key === " ") {
        event.preventDefault();
        show(current + 1);
        closeOverlays();
      }
      return;
    }
    if (key === "ArrowRight" || key === "ArrowDown" || key === " " || key === "PageDown" || key === "n") {
      event.preventDefault();
      next();
    } else if (key === "ArrowLeft" || key === "ArrowUp" || key === "PageUp" || key === "p") {
      event.preventDefault();
      prev();
    } else if (key === "Home") {
      event.preventDefault();
      show(0);
    } else if (key === "End") {
      event.preventDefault();
      show(slides.length - 1);
    } else if (key === "o" || key === "O") {
      event.preventDefault();
      openOverview();
    } else if (key === "?" || key === "h" || key === "H") {
      event.preventDefault();
      openHelp();
    } else if (key === "f" || key === "F") {
      event.preventDefault();
      toggleFullscreen();
    } else if (key === "P" && event.shiftKey) {
      event.preventDefault();
      window.print();
    }
  });

  if (stage) {
    stage.addEventListener("click", (event) => {
      if (event.target.closest("a, button, input, textarea, select")) return;
      const rect = stage.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width;
      if (x > 0.7) next();
      else if (x < 0.3) prev();
    });
  }

  document.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", () => {
      const action = button.getAttribute("data-action");
      if (action === "prev") prev();
      if (action === "next") next();
      if (action === "overview") openOverview();
      if (action === "help") openHelp();
      if (action === "print") window.print();
      if (action === "fullscreen") toggleFullscreen();
    });
  });

  window.addEventListener("resize", fit);
  window.addEventListener("hashchange", () => show(initialIndex(), false));

  fit();
  show(initialIndex(), false);
  buildOverview();

  const ready = () => {
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => setTimeout(runQA, 120));
    } else {
      setTimeout(runQA, 300);
    }
  };
  ready();
  window.addEventListener("load", () => setTimeout(runQA, 250));
})();
