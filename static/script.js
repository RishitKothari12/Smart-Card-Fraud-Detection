// static/script.js — Enhanced UX with smooth interactions

document.addEventListener("DOMContentLoaded", function () {
  
  // Animate elements on page load
  const panels = document.querySelectorAll('.panel');
  panels.forEach((panel, index) => {
    panel.style.opacity = '0';
    panel.style.transform = 'translateY(20px)';
    setTimeout(() => {
      panel.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      panel.style.opacity = '1';
      panel.style.transform = 'translateY(0)';
    }, index * 100);
  });

  // Enhanced select dropdown animation
  document.querySelectorAll("label").forEach(function (lab) {
    const sel = lab.querySelector("select");
    if (!sel) return;

    const startOpen = function () {
      sel.classList.add("open");
      lab.classList.add("open");
    };
    
    const endOpen = function () {
      sel.classList.remove("open");
      lab.classList.remove("open");
    };

    sel.addEventListener("mousedown", startOpen);
    sel.addEventListener("touchstart", startOpen, {passive: true});

    sel.addEventListener("keydown", function (e) {
      if (e.key === " " || e.key === "Enter" || e.key === "ArrowDown" || e.key === "ArrowUp") {
        startOpen();
      }
    });

    sel.addEventListener("blur", endOpen);
    sel.addEventListener("change", endOpen);

    document.addEventListener("click", function (ev) {
      if (!lab.contains(ev.target)) {
        endOpen();
      }
    });
  });

  // Enhanced button interactions
  document.querySelectorAll(".btn").forEach(function(btn) {
    btn.addEventListener("mouseenter", function() {
      btn.style.transform = "translateY(-2px)";
    });
    
    btn.addEventListener("mouseleave", function() {
      btn.style.transform = "";
    });
    
    btn.addEventListener("mousedown", function() {
      btn.style.transform = "translateY(0px)";
    });
    
    btn.addEventListener("mouseup", function() {
      btn.style.transform = "translateY(-2px)";
    });
  });

  // Add focus glow effect to inputs
  const inputs = document.querySelectorAll('input, select, textarea');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.style.transition = 'all 0.3s ease';
    });
  });

  // Form submission animation
  const form = document.querySelector('#demo-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.textContent = 'Analyzing...';
        submitBtn.style.opacity = '0.7';
        submitBtn.style.cursor = 'wait';
      }
    });
  }

  // Smooth scroll behavior
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add subtle parallax effect to panels on scroll
  window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const panels = document.querySelectorAll('.panel');
    panels.forEach((panel, index) => {
      const speed = 0.05 * (index + 1);
      panel.style.transform = `translateY(${scrolled * speed}px)`;
    });
  });
});