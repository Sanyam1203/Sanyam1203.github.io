/* assets/js/motion.js */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Scroll Progress & Navbar
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress-bar';
    document.body.appendChild(progressBar);

    const navbar = document.getElementById('navbar');
    let lastScrollY = window.scrollY;
    let ticking = false;

    function onScroll() {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const currentScrollY = window.scrollY;
                
                // Progress Bar
                const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
                if (scrollHeight > 0) {
                    const progress = Math.min(1, Math.max(0, currentScrollY / scrollHeight));
                    progressBar.style.transform = `scaleX(${progress})`;
                }

                // Navbar Logic
                if (navbar) {
                    if (currentScrollY > 20) {
                        navbar.classList.add('nav-scrolled');
                    } else {
                        navbar.classList.remove('nav-scrolled');
                    }

                    // Only hide navbar if scrolling down past 120px, show if scrolling up
                    // Do not hide if mobile menu is open (assuming #mobile-menu doesn't have 'hidden')
                    const mobileMenu = document.getElementById('mobile-menu');
                    const isMobileMenuOpen = mobileMenu && !mobileMenu.classList.contains('hidden');

                    if (currentScrollY > 120 && currentScrollY > lastScrollY && !isMobileMenuOpen) {
                        navbar.classList.add('nav-hidden');
                    } else if (currentScrollY < lastScrollY || currentScrollY <= 120) {
                        navbar.classList.remove('nav-hidden');
                    }
                }

                lastScrollY = currentScrollY;
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    // Trigger once on load
    onScroll();

    // 2. Reveal System
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (!prefersReducedMotion && 'IntersectionObserver' in window) {
        const revealOptions = {
            root: null,
            rootMargin: '0px 0px -50px 0px',
            threshold: 0.1
        };

        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, revealOptions);

        document.querySelectorAll('.reveal-text, .reveal-fade').forEach(el => {
            revealObserver.observe(el);
        });
    }

    // 3. Mobile Menu Polish
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    if (mobileMenuBtn && mobileMenu && menuIcon) {
        mobileMenuBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.contains('hidden');
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                menuIcon.textContent = 'close';
                mobileMenuBtn.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden'; // prevent background scrolling
            } else {
                closeMobileMenu();
            }
        });

        // Close menu when clicking a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                closeMobileMenu();
            });
        });

        function closeMobileMenu() {
            mobileMenu.classList.add('hidden');
            menuIcon.textContent = 'menu';
            mobileMenuBtn.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }
    }

    // 4. Active Nav Link Detection
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href, window.location.origin).pathname;
        
        // Exact match for root or matching prefixes for subpages
        if (linkPath === currentPath) {
            link.classList.add('active');
        } else if (linkPath !== '/' && linkPath !== '/index.html' && currentPath.startsWith(linkPath)) {
            // E.g., /products/ matches /products/index.html
            link.classList.add('active');
        }
    });
});
