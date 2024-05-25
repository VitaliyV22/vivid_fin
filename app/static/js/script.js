document.addEventListener('DOMContentLoaded', function() {
    // Example JS functionality
    var deleteButtons = document.querySelectorAll('.btn-delete');

    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            var confirmation = confirm("Are you sure you want to delete this item?");
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });
});