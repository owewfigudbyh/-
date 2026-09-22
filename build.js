// Сборка сайта для Timeweb App Platform: складывает готовые файлы в папку dist.
const fs = require('fs');
const path = require('path');

const OUT = 'dist';

const FILES = [
  'index.html',
  'obmen-rub-uah.html',
  'perestanovka-nalichnyh.html',
  '404.html',
  'styles.css',
  'favicon.ico',
  'robots.txt',
  'sitemap.xml',
];

const DIRS = ['img'];

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

let count = 0;
for (const file of FILES) {
  if (fs.existsSync(file)) {
    fs.copyFileSync(file, path.join(OUT, file));
    count++;
  }
}
for (const dir of DIRS) {
  if (fs.existsSync(dir)) {
    fs.cpSync(dir, path.join(OUT, dir), { recursive: true });
    count += fs.readdirSync(dir).length;
  }
}

console.log(`Готово: ${count} файлов в папке ${OUT}`);
