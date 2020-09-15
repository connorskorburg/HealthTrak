const loginForm = document.getElementById('login-pop-outer');
const loginMobileBtn = document.getElementById('login-mobile');
const loginBtn = document.getElementById('login-button');


const closeLog = document.getElementById('close-login-form');


function showLogForm(btn) {
  btn.addEventListener('click', () => {
    loginForm.style.display = 'block';
  })
}


function closeForm (btn) {
  btn.addEventListener('click', () => {
    loginForm.style.display = 'none';
    regForm.style.display = 'none';
  })
}


showLogForm(loginMobileBtn);
showLogForm(loginBtn);

closeForm(closeLog);