function previewImage(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('image-preview');
    const previewContainer = document.getElementById('image-preview-container');
    
    if (file) {
        // Validar tipo de archivo
        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            alert('Por favor, selecciona un formato de imagen válido (JPG, PNG, GIF, WebP)');
            event.target.value = '';
            previewContainer.classList.add('hidden');
            return;
        }
        
        // Validar tamaño (máx 5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert('La imagen no puede superar 5MB');
            event.target.value = '';
            previewContainer.classList.add('hidden');
            return;
        }
        
        // Mostrar preview
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
}

function clearImagePreview() {
    document.getElementById('imagen_archivo').value = '';
    document.getElementById('image-preview-container').classList.add('hidden');
    document.getElementById('image-preview').src = '';
}