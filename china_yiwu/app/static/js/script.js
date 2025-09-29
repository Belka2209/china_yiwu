document.addEventListener('DOMContentLoaded', function() {
    // Открытие попапа
    const popupLinks = document.querySelectorAll('[href^="#popup"]');
    const popupClose = document.querySelector('.popup__close');
    const popup = document.getElementById('popup-form');
    
    popupLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            popup.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });
    
    popupClose.addEventListener('click', function(e) {
        e.preventDefault();
        popup.style.display = 'none';
        document.body.style.overflow = '';
    });
    
    // Закрытие попапа при клике вне его
    popup.addEventListener('click', function(e) {
        if (e.target === popup) {
            popup.style.display = 'none';
            document.body.style.overflow = '';
        }
    });
    
    // Плавная прокрутка для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 70,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Мобильное меню (можно добавить при необходимости)
});