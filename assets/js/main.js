const revealItems = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

revealItems.forEach((item) => observer.observe(item));

document.querySelector('[data-random-pick]')?.addEventListener('click', (event) => {
  const slugs = event.currentTarget.dataset.products.split(',').filter(Boolean);
  const pick = slugs[Math.floor(Math.random() * slugs.length)];
  window.location.href = `products/${pick}.html`;
});

document.querySelectorAll('[data-back-top]').forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
