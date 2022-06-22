// main page js

const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar-menu');
const navLogo = document.querySelector('#navbar-logo');
// const form = document.querySelector('main-form');

// display  mobile menu
const mobilemenu = () => {
  menu.classList.toggle('is-active');
  menuLinks.classList.toggle('active');
};

menu.addEventListener('click', mobilemenu);

const highlightMenu = () => {
  const elem = document.querySelector('.highlight');
  const homePage = document.querySelector('#homePage');
  const aboutPage = document.querySelector('#aboutPage');

  const featurePage = document.querySelector('#featurePage');
  const signUpPage = document.querySelector('#signupPage');
  let scrollPos = window.scrollY;
  // console.log(scrollPos);

  // adds 'highlight' class to my menu items
  if (window.innerWidth > 960 && scrollPos < 600) {
    homePage.classList.add('highlight');
    aboutPage.classList.remove('highlight');
    featurePage.classList.remove('highlight');
    return;
  } else if (window.innerWidth > 960 && scrollPos < 1400) {
    homePage.classList.remove('highlight');
    featurePage.classList.add('highlight');
    aboutPage.classList.remove('highlight');
    homePage.classList.remove('highlight');

    return;
  } else if (window.innerWidth > 960 && scrollPos < 2345) {
    featurePage.classList.remove('highlight');
    aboutPage.classList.add('highlight');
    homePage.classList.remove('highlight');

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

function results(form) {
  let x = form.address.value;
  alert(x);
}

function toDashboard(form) {
  let x = form.address.value;
  location.href = '/dashboard/' + x;
  alert('dashboard loading');
}

// form animations
const inputs = document.querySelectorAll('input');

inputs.forEach((el) => {
  el.addEventListener('blur', (e) => {
    if (e.target.value) {
      e.target.classList.add('dirty');
    } else {
      e.target.classList.remove('dirty');
    }
  });
});

//label effects
$(window).load(function () {
  $('.form-bar input').val('');

  $('.input-effect input').focusout(function () {
    if ($(this).val() != '') {
      $(this).addClass('has-content');
    } else {
      $(this).removeClass('has-content');
    }
  });
});

// Parallax for Eth Logo
// window.addEventListener('scroll', function (e) {
//   const target = document.querySelectorAll('ethlogo');
//   var index = 0;
//   var length = target.length;

//   for (index; index < length; index++) {
//     var posY = window.scrollY * target[index].dataset.ratey;
//     var posX = window.scrollY * target[index].dataset.ratex;
//     var direction = target[index].dataset.direction;

//     if (direction === 'left') {
//       target.style.transform =
//         'translate3d(' + posX + 'px,' + posY + 'px, 5px)';
//     } else {
//       target.style.transform =
//         'translate3d(' + posX + 'px,' + posY + 'px, 5px)';
//     }
//   }
// });

// parallax for  eth symbol LEFT
window.addEventListener('scroll', function (e) {
  const target = document.querySelector('#ethlogo-left');
  var posY = window.scrollY * target.dataset.ratey;
  var posX = window.scrollY * target.dataset.ratex;
  target.style.transform = 'translate3d(' + posX + 'px,' + posY + 'px, 5px)';
});

// parallax for eth symbol RIGHT
window.addEventListener('scroll', function (e) {
  const target = document.querySelector('#ethlogo-right');
  var posY = window.scrollY * target.dataset.ratey;
  var posX = window.scrollY * target.dataset.ratex;
  target.style.transform = 'translate3d(' + posX + 'px,' + posY + 'px, 5px)';
});
// SVG
// let path = document.querySelectorAll('line');
// let index = 0;
// var length = path.length;

// window.addEventListener('scroll', ()=>{
//   for(index; index < length; index++){
//     path[index].length
//   }
//   var scrollPercentage = (document.documentElement.scrollTop + document.body.scrollTop)
//   var drawlength = length * scrollPercentage;
//   path.style.strokeDashOffset = length - drawlength;
// });

// Parallax for Features
// window.addEventListener('scroll', function(e) {

//   const target = document.querySelectorAll('.features-card');
//   console.log(target[1].style);
//   var index = 0;
//   var length = target.length;
//   var scrollPos = this.scrollY;
//   if(scrollPos > 1200){
//     for(index; index < length; index++){
//       var posY = window.scrollY * target[index].dataset.y;
//       var posX = window.scrollY * target[index].dataset.x;
//       var direction = target[index].dataset.direction;

//       if(direction === 'left'){
//         target[index].style.transform = 'translate3d('+posX+'px, 5px, 5px)';
//       } else {
//         target[index].style.transform = 'translate3d('+posX+'px, '+posY+'px, 5px)';
//       }
//     }
//   }
//   // target.style.transform = 'translate3d(5px, 5px, 5px)';
//   // var pos = window.scrollY * target[index].dataset.rate;
//   // target.style.transform = 'translate3d(5px, '+pos+'px, 5px)';

// });
