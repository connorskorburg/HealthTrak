const mobileNav = document.getElementById('home-nav-mobile');
document.getElementById('hamburger').addEventListener('click', () => {
  if(mobileNav.style.display === '' || mobileNav.style.display === 'none') {
    mobileNav.style.display = 'block';
  } else if (mobileNav.style.display === 'block') {
    mobileNav.style.display = 'none';
  }
});