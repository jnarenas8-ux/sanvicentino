// Animación fade para las tarjetas
document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll('.animate-fade');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        entry.target.classList.add('opacity-100', 'translate-y-0');
        entry.target.classList.remove('opacity-0', 'translate-y-4');
      }
    });
  });

  items.forEach(item => {
    item.classList.add('opacity-0', 'translate-y-4', 'transition', 'duration-500');
    observer.observe(item);
  });

  // Menú móvil toggle
  const toggle = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  toggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });
});
