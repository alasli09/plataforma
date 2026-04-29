function actualizarContador() {
    const ahora = new Date();
    const cierre = new Date();
    cierre.setHours(16, 0, 0); // 4:00 PM

    if (ahora > cierre) {
        document.getElementById('label-reloj').innerText = "Ventana Cerrada";
        document.getElementById('countdown').innerText = "00:00:00";
        return;
    }

    const diff = cierre - ahora;
    const horas = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const mins = Math.floor((diff / (1000 * 60)) % 60);
    const segs = Math.floor((diff / 1000) % 60);

    document.getElementById('countdown').innerText = 
        `${horas.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${segs.toString().padStart(2, '0')}`;
}

setInterval(actualizarContador, 1000);

document.getElementById('nominacion-form').onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        contrato: document.getElementById('contrato').value,
        cantidad: document.getElementById('cantidad').value
        // Agregar los demás campos aquí
    };

    const response = await fetch('/nominar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.error) {
        alert("ERROR: " + result.error);
    } else {
        alert("ÉXITO: " + result.message);
    }
};
