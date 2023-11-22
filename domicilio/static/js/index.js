new DataTable('#cars');
new DataTable('#records');
new DataTable('#category');
new DataTable('#measurement_unit');
new DataTable('#elements');
new DataTable('#inventories');
new DataTable('#domicilies');
var errorMessage = document.getElementById('error-message').innerText;
// Verifica si hay un error y muestra un mensaje si lo hay
if (errorMessage) {
    swal({
        title: "Error",
        text: errorMessage,
        icon: "error",
    });
}