const images = Array.from(document.querySelectorAll('img'), (img, i) => ({
  index: i,
  src: img.src.split('/').pop(),
  naturalWidth: img.naturalWidth,
  naturalHeight: img.naturalHeight,
  offsetLeft: img.offsetLeft,
  offsetTop: img.offsetTop,
  clientWidth: img.clientWidth,
  clientHeight: img.clientHeight,
}));
console.log(JSON.stringify({ viewport: { w: window.innerWidth, h: window.innerHeight }, images }));
