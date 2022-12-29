// 获取图片的 base64
export function getBase64(img, callback) {
  const reader = new FileReader();

  reader.addEventListener('load', () =>
    callback(reader.result)
  );

  reader.readAsDataURL(img);
}

// 时间格式化
export function formatTime(datetime) {
  const d = new Date(datetime);
  const yyyy = d.getFullYear();
  const mm = d.getMonth() + 1;
  const dd = d.getDate();
  const h = d.getHours();
  const m = d.getMinutes();

  return `${yyyy}年${mm}月${dd}日 ${h}:${m}`;
}
