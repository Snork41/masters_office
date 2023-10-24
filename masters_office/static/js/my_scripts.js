// bootstrap Tooltips (на кнопках "редактировать запись", "следущая/предыдущая запись")
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
// получаем текущее значение из localStorage
let currentText = localStorage.getItem("currentText");
// если значение не пустое (т.е. уже было сохранено ранее)
if (currentText) {
  // устанавливаем текст на кнопке
  document.querySelector(".btn-outline-danger").innerHTML = currentText;
}
function changeText() {
  if (currentText === "Пометить на удаление") {
    currentText = "Отменить удаление";
  } else {
    currentText = "Пометить на удаление";
  }
    // сохраняем новое значение в localStorage
  localStorage.setItem("currentText", currentText);
  
  document.querySelector(".btn-outline-danger").innerHTML = currentText;
}


// for bootstrap Toast show
// const toastContent = document.querySelector('.toast');
// const toast = new bootstrap.Toast(toastContent);
// toast.show();