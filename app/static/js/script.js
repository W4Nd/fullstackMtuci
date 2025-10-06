// Обработка формы добавления напоминания
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reminderForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const days = [];
            formData.getAll('days').forEach(day => days.push(parseInt(day)));
            
            const reminderData = {
                medication_name: formData.get('medication_name'),
                dosage: formData.get('dosage'),
                time: formData.get('time'),
                days: days
            };
            
            fetch('/api/reminders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reminderData)
            })
            .then(response => response.json())
            .then(data => {
                alert('Напоминание добавлено!');
                form.reset();
                window.location.href = '/reminders';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ошибка при добавлении напоминания');
            });
        });
    }
});

// Удаление напоминания
function deleteReminder(reminderId) {
    if (confirm('Вы уверены, что хотите удалить это напоминание?')) {
        fetch(`/api/reminders/${reminderId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert('Напоминание удалено!');
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка при удалении напоминания');
        });
    }
}

// Включение/выключение напоминания
function toggleReminder(reminderId) {
    fetch(`/api/reminders/${reminderId}/toggle`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка при изменении статуса напоминания');
    });
}