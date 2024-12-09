// Изменение иконки пользователя
document.querySelectorAll('#user-icon').forEach(item => {
    item.addEventListener('mouseover', () => {
        item.src = "/static/main/img/icon-user-red.png"; // Иконка при наведении
    });
    item.addEventListener('mouseout', () => {
        item.src = "/static/main/img/icon-user.png"; // Возврат к исходной иконке
    });
});

// Изменение иконки поиска
document.querySelectorAll('.icon-search').forEach(item => {
    item.addEventListener('mouseover', () => {
        item.src = "/static/main/img/icon-search-red.png"; // Иконка при наведении
    });
    item.addEventListener('mouseout', () => {
        item.src = "/static/main/img/icon-search.png"; // Возврат к исходной иконке
    });
});
