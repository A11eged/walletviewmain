// main page js

const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar-menu')
const navLogo = document.querySelector('#navbar-logo');
// const form = document.querySelector('main-form');

// display  mobile menu
const mobilemenu = () => {
  menu.classList.toggle('is-active')
  menuLinks.classList.toggle('active')
}

menu.addEventListener('click', mobilemenu)

const highlightMenu = () => {
  const elem = document.querySelector('.highlight');
  const homePage = document.querySelector('#homePage');
  const aboutPage = document.querySelector('#aboutPage');

  const featurePage = document.querySelector('#featurePage');
  const signUpPage = document.querySelector('#signupPage');
  let scrollPos = window.scrollY;

  if (window.innerWidth > 960 && scrollPos < 600) {
    homePage.classList.add('highlight');
    aboutPage.classList.remove('highlight');
    featurePage.classList.remove('highlight');
    return;
  } 
    else if (window.innerWidth > 960 && scrollPos < 1400) {
    homePage.classList.remove('highlight');
    featurePage.classList.add('highlight');
    aboutPage.classList.remove('highlight');
    homePage.classList.remove('highlight');

    return;
  } 
    else if (window.innerWidth > 960 && scrollPos < 2345) {
    featurePage.classList.remove('highlight');
    aboutPage.classList.add('highlight');
    homePage.classList.remove('highlight');
    signUpPage.classList.remove('highlight');    

    return;
  }
    else if (window.innerWidth > 960 && scrollPos < 3800) {
    featurePage.classList.remove('highlight');
    signUpPage.classList.add('highlight');
    aboutPage.classList.remove('highlight');
    return;
  }

  if ((elem && window.innerWidth < 960 && scrollPos < 600) || elem) {
    elem.classList.remove('highlight');
  }
};

window.addEventListener('scroll', highlightMenu);
window.addEventListener('click', highlightMenu);

//  Close mobile Menu when clicking on a menu item
const hideMobileMenu = () => {
  const menuBars = document.querySelector('.is-active');
  if (window.innerWidth <= 768 && menuBars) {
    menu.classList.toggle('is-active');
    menuLinks.classList.remove('active');
  }
};

menuLinks.addEventListener('click', hideMobileMenu);
navLogo.addEventListener('click', hideMobileMenu);

//redirect

function results(form){
  let x = form.address.value;
  alert (x);
}

function toDashboard(form){
  let x = form.address.value;
  location.href = "/dashboard/" + x;
  alert("dashboard loading");
}

// form animations
// const inputs = document.querySelectorAll('input');

// inputs.forEach(el => {
//   el.addEventListener('blur', e => {
//     if(e.target.value) {
//       e.target.classList.add('dirty');
//     } else {
//       e.target.classList.remove('dirty');
//     }
//   })
// })

//label effects
$(window).load(function(){
  $(".form-bar input").val("");
  $(".input-effect").focusout(function(){
    if($(this).val() != ""){
      $(this).addClass("has-content");
    }else{
      $(this).removeClass("has-content");
    }
  })
});

console.log('script.js says "I\'m here"');
