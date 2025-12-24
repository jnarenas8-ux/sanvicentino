

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('menu-toggle');
  const menu = document.getElementById('menu');
  if (!toggle || !menu) return;

  // Animación hamburguesa
  toggle.addEventListener('click', () => {
    menu.classList.toggle('hidden');
    menu.classList.toggle('animate-fade-in');
    toggle.classList.toggle('open');
    toggle.classList.toggle('group-open');
  });

  // Cerrar menú al hacer clic fuera (solo móvil)
  document.addEventListener('click', (e) => {
    if (window.innerWidth >= 768) return;
    if (!menu.contains(e.target) && !toggle.contains(e.target)) {
      if (!menu.classList.contains('hidden')) {
        menu.classList.add('hidden');
        toggle.classList.remove('open', 'group-open');
      }
    }
  });

  // Animación fade-in
  if (!menu.classList.contains('hidden')) {
    menu.classList.add('animate-fade-in');
  }
});


// Animación fade-in para cada sección al entrar en viewport
document.addEventListener('DOMContentLoaded', function () {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('opacity-100');
        entry.target.classList.remove('opacity-0');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.fade-section').forEach(section => {
    observer.observe(section);
  });
});


// Galería tipo abanico con deslizamiento automático y responsive
document.addEventListener('DOMContentLoaded', function () {
  const images = document.querySelectorAll('#fan-images .fan-img');
  let current = 0;
  function updateFan() {
    images.forEach((img, i) => {
      const offset = i - current;
      // Responsive: valores según ancho de pantalla
      let rotate = 20 * offset;
      let scale = offset === 0 ? 1.1 : 0.9;
      let translateX = 0;
      if (window.innerWidth < 640) {
        // Móvil: menos separación y tamaño
        translateX = offset * 40;
        img.style.width = '90px';
        img.style.height = '120px';
      } else if (window.innerWidth < 1024) {
        // Tablet
        translateX = offset * 60;
        img.style.width = '120px';
        img.style.height = '170px';
      } else {
        // Desktop
        translateX = offset * 80;
        img.style.width = '160px';
        img.style.height = '224px';
      }
      img.style.position = 'absolute';
      img.style.left = '50%';
      img.style.top = '50%';
      img.style.objectFit = 'cover';
      img.style.borderRadius = '0.75rem';
      img.style.boxShadow = '0 4px 24px 0 rgba(0,0,0,0.10)';
      img.style.transition = 'transform 0.7s cubic-bezier(0.4,0,0.2,1), opacity 0.4s, z-index 0.2s';
      img.style.transform = `translate(-50%, -50%) rotate(${rotate}deg) scale(${scale}) translateX(${translateX}px)`;
      img.style.zIndex = 3 - Math.abs(offset);
      img.style.opacity = Math.abs(offset) > 1 ? 0 : 1;
    });
  }
  function nextFan() {
    current = (current + 1) % images.length;
    updateFan();
  }
  updateFan();
  setInterval(nextFan, 2200);
  window.addEventListener('resize', updateFan);
});