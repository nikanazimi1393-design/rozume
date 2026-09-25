// تم شب/روز + انیمیشن ظاهر شدن + تایپینگ
const btn = document.getElementById('themeBtn');
if (localStorage.theme === 'light') document.body.classList.add('light');
btn.onclick = () => {
  document.body.classList.toggle('light');
  localStorage.theme = document.body.classList.contains('light') ? 'light' : 'dark';
  btn.textContent = document.body.classList.contains('light') ? '☀️' : '🌙';
};
btn.textContent = document.body.classList.contains('light') ? '☀️' : '🌙';

const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) e.target.classList.add('in');
}), {threshold: .1});
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// فیلتر نمونه‌کارها (بدون نیاز به سرور)
const filters = document.getElementById('filters');
if (filters) {
  filters.addEventListener('click', e => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    document.querySelectorAll('#filters .chip').forEach(c => c.classList.remove('on'));
    chip.classList.add('on');
    const f = chip.dataset.filter;
    document.querySelectorAll('#projectGrid .card').forEach(card => {
      card.style.display = (f === 'همه' || card.dataset.cat === f) ? '' : 'none';
    });
  });
}
const tw = document.getElementById('typing');
if (tw) {
  const texts = [tw.textContent, 'عاشق پایتون 🐍', 'سازنده ابزارهای کاربردی 🛠', 'دنبال پروژه واقعی 🚀'];
  let i = 0, j = 0, del = false;
  setInterval(() => {
    const full = texts[i];
    j += del ? -1 : 1;
    tw.textContent = full.slice(0, j);
    if (!del && j >= full.length) { del = true; setTimeout(()=>{}, 400); }
    if (del && j <= 0) { del = false; i = (i+1) % texts.length; }
  }, 90);
}
