export function log(msg: any, ...optionalParams: any[]) {
  if (import.meta.env.DEV) {
    console.log(msg, ...optionalParams);
  }
}
