// 获取图片的 base64
type Callback = (base64Url: string) => void;

export function getBase64(img: Blob, callback: Callback) {
  const reader = new FileReader();

  reader.addEventListener('load', () => callback(reader.result as string));

  reader.readAsDataURL(img);
}
