document.addEventListener('DOMContentLoaded', () => {
      const toggleButton = document.getElementById('mobile-menu-toggle');
      const mobileMenu = document.getElementById('mobile-menu');

      toggleButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
      });
    });