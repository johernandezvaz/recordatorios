// JavaScript personalizado para el Sistema de Calidad

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss para mensajes de alerta después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirmación para acciones destructivas
    const destructiveButtons = document.querySelectorAll('[data-confirm]');
    destructiveButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || '¿Está seguro de realizar esta acción?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });

    // Función para actualizar el estado de los recordatorios en tiempo real
    function updateRecordatorioStatus() {
        const recordatorios = document.querySelectorAll('[data-fecha-proxima]');
        const now = new Date();
        
        recordatorios.forEach(function(elemento) {
            const fechaProxima = new Date(elemento.getAttribute('data-fecha-proxima'));
            const diffTime = fechaProxima - now;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            // Actualizar clases CSS según el estado
            elemento.classList.remove('table-danger', 'table-warning');
            
            if (diffDays < 0) {
                elemento.classList.add('table-danger');
            } else if (diffDays <= 7) {
                elemento.classList.add('table-warning');
            }
        });
    }

})