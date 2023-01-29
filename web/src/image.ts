export const headers = {
  'X-API-Key': import.meta.env.VITE_IMAGE_UPLOAD_TOKEN,
};

// 从图床返回值中获取 url 地址
export function getImageUrl(resp: any) {
  return resp.image.url as string;
}

// 从图床返回值中获取图片名
export function getImageName(resp: any) {
  return resp.image.image.name;
}
