function mostrarDescripcion(id) {
  const secciones = ['belleza', 'familia', 'medio'];
  secciones.forEach(sec => {
    const el = document.getElementById(`descripcion-${sec}`);
    if (el) el.classList.add('hidden');
  });
  const activo = document.getElementById(`descripcion-${id}`);
  if (activo) {
    activo.classList.remove('hidden');
    activo.classList.add('animate-fade-in');
  }
}

