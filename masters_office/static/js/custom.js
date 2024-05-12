// bootstrap Tooltips (на кнопках "редактировать запись", "следущая/предыдущая запись")
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


// Стрелка возврата в верх страницы
$(window).scroll(function() {
    if ($(this).scrollTop() > 500) {
        $('.scroll-to-top').fadeIn();
    } else {
        $('.scroll-to-top').fadeOut();
    }
}).scroll();

$('.scroll-to-top').click(function(event) {
    event.preventDefault();
    $('html, body').animate({scrollTop: 0}, 300);
});


// for bootstrap Toast show
// const toastContent = document.querySelector('.toast');
// const toast = new bootstrap.Toast(toastContent);
// toast.show();


// Кнопка "Пометить на удаление"
document.addEventListener('DOMContentLoaded', function () {
    let button = document.querySelector('.btn-delete-post');
    if (button !== null) {
        button.addEventListener('click', function () {
            if (button.textContent.toLowerCase().includes("пометить")) {
                button.textContent = "Помечено на удаление";
            } else {
                button.textContent = "Пометить на удаление";
            }
        });
    }
});

// Удаление уведомления по нажатию на крестик
document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const countNotifications = document.querySelector('.peending');
    const modalNotificationsNontent = document.querySelector('.modal-notifications-content');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const notificationId = this.getAttribute('data-notification-id');
            let formData = new FormData();
            formData.append('id', notificationId);

            fetch('core/view_notification/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    this.closest('.row').remove();
                    let newCountNotifications = parseInt(countNotifications.textContent) - 1
                    if (newCountNotifications === 0) {
                        countNotifications.remove()
                        modalNotificationsNontent.textContent = 'Новых уведомлений нет'
                    } else {
                        countNotifications.textContent = newCountNotifications                        
                    }
                } else {
                    alert(data.message);
                }
            });
        });
    });
});