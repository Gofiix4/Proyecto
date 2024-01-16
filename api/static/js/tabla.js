document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("buscador");
    const tabla = document.getElementById("miTabla");
    const filas = tabla.getElementsByTagName("tr");

    input.addEventListener("keyup", function () {
        const filtro = input.value.toLowerCase();

        for (let i = 1; i < filas.length; i++) {
            const fila = filas[i];
            const celdas = fila.getElementsByTagName("td");
            let mostrarFila = false;

            for (let j = 0; j < celdas.length; j++) {
                const celda = celdas[j];

                if (celda) {
                    const contenido = celda.textContent.toLowerCase();

                    if (contenido.indexOf(filtro) > -1) {
                        mostrarFila = true;
                        break;
                    }
                }
            }

            if (mostrarFila) {
                fila.style.display = "";
            } else {
                fila.style.display = "none";
            }
        }
    });
});
