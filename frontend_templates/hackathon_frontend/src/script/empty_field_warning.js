document.getElementById('signinForm').addEventListener('submit', function(event) {
      event.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      const errorMessage = document.getElementById('errorMessage');

      if (!email || !password) {
        errorMessage.classList.remove('hidden');
      } else {
        errorMessage.classList.add('hidden');
        // Proceed with actual sign in logic here
        console.log('Signing in with:', { email, password });
      }
    });