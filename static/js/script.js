// Función del Contador para las 4:00 PM (16:00)
function updateTimer() {
    const now = new Date();
    const closure = new Date();
    closure.setHours(16, 0, 0, 0);

    // Si ya pasaron las 4 PM, el contador apunta a las 4 PM de mañana
    if (now > closure) {
        closure.setDate(closure.getDate() + 1);
    }

    const diff = closure - now;
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / 1000 / 60) % 60);
    const seconds = Math.floor((diff / 1000) % 60);

    document.getElementById('timer').innerText = 
        `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

setInterval(updateTimer, 1000);
updateTimer();

// Manejo del envío del Formulario
document.getElementById('form-nominacion').addEventListener('submit', async (e) => {
    e.preventDefault();

    const contrato = document.getElementById('contrato').value;
    const cantidad = document.getElementById('cantidad').value;
    const fecha = document.getElementById('fecha').value;

    try {
        const response = await fetch('/enviar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contrato, cantidad, fecha })
        });

        const result = await response.json();

        if (result.status === 'success') {
            alert('✅ Success: ' + result.message);
            document.getElementById('form-nominacion').reset();
            // Re-poner la fecha de hoy tras resetear
            document.getElementById('fecha').value = new Date().toISOString().split('T')[0];
        } else {
            alert('❌ ' + result.message);
        }
    } catch (error) {
        alert('❌ Error de conexión con el servidor.');
    }
});
