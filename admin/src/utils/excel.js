export function exportExcel(data, filename) {
  let url = window.URL.createObjectURL(new Blob([data]));
  let link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `${filename}.xlsx`);
  document.body.appendChild(link);
  link.click();
}