// bootstrap Tooltips (на кнопках "редактировать запись", "следущая/предыдущая запись")
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


// for bootstrap Toast show
// const toastContent = document.querySelector('.toast');
// const toast = new bootstrap.Toast(toastContent);
// toast.show();