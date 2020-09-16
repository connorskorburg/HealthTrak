const loginForm = document.getElementById('login-pop-outer');
const loginMobileBtn = document.getElementById('login-mobile');
const loginBtn = document.getElementById('login-button');
const mailCard = document.getElementById('mail-card');

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

document.getElementById('mail-btn').addEventListener('click', () => {
  if(mailCard.style.display === '' || mailCard.style.display == 'none') {
    mailCard.style.display = 'flex';
  } else if (mailCard.style.display === 'flex') {
    mailCard.style.display = 'none';
  }
});