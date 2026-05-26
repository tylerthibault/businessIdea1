// Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
  [].forEach.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'), function(el) {
    new bootstrap.Tooltip(el);
  });
  // Auto-dismiss flash messages
  setTimeout(function() {
    document.querySelectorAll('.alert-dismissible').forEach(function(a) {
      new bootstrap.Alert(a).close();
    });
  }, 4000);
});
