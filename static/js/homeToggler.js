const loginForm = document.getElementById('login-pop-outer');
const regForm = document.getElementById('reg-pop-outer');
const loginMobileBtn = document.getElementById('login-mobile');
const loginBtn = document.getElementById('login-button');

const regMobileBtn = document.getElementById('reg-mobile');
const regBtn = document.getElementById('reg-button');

const closeReg = document.getElementById('close-reg-form');
const closeLog = document.getElementById('close-login-form');


function showLogForm(btn) {
  btn.addEventListener('click', () => {
    loginForm.style.display = 'block';
  })
}

function showRegForm(btn) {
  btn.addEventListener('click', () => {
    regForm.style.display = 'block';
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

showRegForm(regMobileBtn);
showRegForm(regBtn);

closeForm(closeReg);
closeForm(closeLog);