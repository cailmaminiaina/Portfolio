document.addEventListener("DOMContentLoaded", () => {
    const loader = document.querySelector(".loader");
    if (loader) {
        setTimeout(() => {
            loader.classList.add("hidden");
            document.body.style.overflow = "visible";
        }, 2000);
    }
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        } else {
            console.warn(`Aucune cible trouvée pour ${this.getAttribute('href')}`);
        }
    });
});
AOS.init({
    startEvent: 'load',
    duration: 1000, 
    easing: 'ease-out', 
    once: false 
});
