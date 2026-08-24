document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => {
  document.querySelectorAll('.tab, .form').forEach(el => el.classList.remove('active'));
  tab.classList.add('active'); document.getElementById(tab.dataset.tab).classList.add('active');
}));
