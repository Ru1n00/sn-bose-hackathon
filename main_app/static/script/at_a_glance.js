function animateCounters() {
    const counters = document.querySelectorAll('[data-target]');
    counters.forEach(counter => {
      const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        const current = +counter.innerText;
        const increment = target / 100;

        if (current < target) {
          counter.innerText = Math.ceil(current + increment);
          setTimeout(updateCount, 15);
        } else {
          counter.innerText = target + "+";
        }
      };
      updateCount();
    });
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounters();
        observer.disconnect();
      }
    });
  });

  observer.observe(document.querySelector('#at-a-glance'));
