document.addEventListener('DOMContentLoaded', function() {
    // Insertar el HTML del modal en el cuerpo del documento
    var modalHTML = `
        <div id="evidenceModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <img src="" alt="Evidencia" id="evidenceImage">
            </div>
        </div>`;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    var modal = document.getElementById("evidenceModal");
    var modalImg = document.getElementById("evidenceImage");
    var span = document.getElementsByClassName("close")[0];

    // Agregar evento click a todos los elementos con la clase 'view-evidence'
    document.querySelectorAll('.view-evidence').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();
            var url = this.getAttribute('data-url');
            modalImg.src = url;
            modal.style.display = "block";
            setTimeout(function() {
                modal.classList.add("show");
            }, 10); // Permitir tiempo para la transición
        });
    });

    // Cerrar el modal al hacer clic en el span (x)
    span.onclick = function() {
        modal.classList.remove("show");
        setTimeout(function() {
            modal.style.display = "none";
        }, 300); // Esperar la duración de la transición
    }

    // Cerrar el modal al hacer clic fuera del contenido del modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.classList.remove("show");
            setTimeout(function() {
                modal.style.display = "none";
            }, 300); // Esperar la duración de la transición
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const toggleMenu = document.getElementById("toggle-premios");
    const submenu = document.getElementById("submenu-premios");
    
    // Check local storage for menu state
    if (localStorage.getItem("submenu-premios-open") === "true") {
        submenu.classList.add("open");
    }

    toggleMenu.addEventListener("click", function() {
        submenu.classList.toggle("open");
        
        // Save state to local storage
        if (submenu.classList.contains("open")) {
            localStorage.setItem("submenu-premios-open", "true");
        } else {
            localStorage.setItem("submenu-premios-open", "false");
        }
    });
});
