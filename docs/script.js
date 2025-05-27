
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.querySelectorAll('.navbar a');
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const themeIndicator = document.getElementById('themeIndicator');

  hamburger.addEventListener('click', () => {
    document.getElementById('navbar').classList.toggle('open');
  });

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      document.getElementById('navbar').classList.remove('open');
    });
  });

  themeToggle.addEventListener('click', () => {
    const isDark = document.body.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcon(isDark);
    updateIndicatorPosition(isDark);
  });

  window.addEventListener('DOMContentLoaded', () => {
    const storedTheme = localStorage.getItem('theme');
    const isDark = storedTheme === 'dark';
    if (isDark) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
    updateThemeIcon(isDark);
    updateIndicatorPosition(isDark);
  });

  function updateThemeIcon(isDark) {
    if (isDark) {
      themeIcon.classList.remove('fa-sun');
      themeIcon.classList.add('fa-moon');
    } else {
      themeIcon.classList.remove('fa-moon');
      themeIcon.classList.add('fa-sun');
    }
  }

  function updateIndicatorPosition(isDark) {
    themeIndicator.style.left = isDark ? '28px' : '4px';
  }
  document.addEventListener('click', function(e) {
   const navbar = document.getElementById('navbar');
    if (navbar.classList.contains('open') && !navbar.contains(e.target)) {
     navbar.classList.remove('open');
    }
  });
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          obs.unobserve(entry.target); 
        }
      });
    },
    {
    threshold: 0.15 
    }
  );

  document.querySelectorAll('.fade-section').forEach(section => {
    observer.observe(section);
});

