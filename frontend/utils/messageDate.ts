export default (d: Date): string => {
  const thisYear = new Date().getFullYear();
  const year = d.getFullYear();
  const dayWithMonth = d.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
  });
  return year === thisYear ? dayWithMonth : `${dayWithMonth}, ${year}`;
}
