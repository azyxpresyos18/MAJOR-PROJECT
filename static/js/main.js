// Demo-District – main.js
// Auto-dismiss messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.msg').forEach(msg => {
    setTimeout(() => {
      msg.style.transition = 'opacity 0.4s';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 400);
    }, 4000);
  });
});
