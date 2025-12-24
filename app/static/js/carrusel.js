
document.addEventListener('DOMContentLoaded', () => {
  const carrusel = document.getElementById('carrusel');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const indicators = document.querySelectorAll('.carousel-indicator');
  if (!carrusel) return;

  let index = 0;
  let intervalo;
  const items = carrusel.children;
  const total = items.length;

  function updateCarrusel() {
    carrusel.style.transform = `translateX(-${index * 100}%)`;
    indicators.forEach((btn, i) => {
      btn.classList.toggle('bg-blue-700', i === index);
      btn.classList.toggle('scale-125', i === index);
      btn.classList.toggle('ring-2', i === index);
      btn.classList.toggle('ring-blue-400', i === index);
    });
  }

  function avanzarCarrusel() {
    index = (index + 1) % total;
    updateCarrusel();
  }

  function retrocederCarrusel() {
    index = (index - 1 + total) % total;
    updateCarrusel();
  }

  function irASlide(i) {
    index = i;
    updateCarrusel();
  }

  function iniciarAnimacion() {
    intervalo = setInterval(avanzarCarrusel, 4000);
  }

  function detenerAnimacion() {
    clearInterval(intervalo);
  }

  if (prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => {
      retrocederCarrusel();
      detenerAnimacion();
      iniciarAnimacion();
    });
    nextBtn.addEventListener('click', () => {
      avanzarCarrusel();
      detenerAnimacion();
      iniciarAnimacion();
    });
  }

  indicators.forEach((btn, i) => {
    btn.addEventListener('click', () => {
      irASlide(i);
      detenerAnimacion();
      iniciarAnimacion();
    });
  });

  carrusel.addEventListener('mouseenter', detenerAnimacion);
  carrusel.addEventListener('mouseleave', iniciarAnimacion);

  updateCarrusel();
  iniciarAnimacion();
});
