"use strict";
let resize = document.getElementById("resize-sec1");
let resize1 = document.getElementById("resize-sec2");
let resize2 = document.getElementById("resize-sec3");
window.onresize = function () {
  if (window.innerWidth <= 1000) {
    resize.style =
      "padding: 20px;margin-left: 20px;margin-right: 20px;margin-top: 50px;padding-left: 50px;padding-right: 50px;";
    resize1.style =
      "padding: 20px;margin-left: 20px;margin-right: 20px;margin-top: 50px;padding-left: 50px;padding-right: 50px;";
    resize2.style =
      "padding: 20px;margin-left: 20px;margin-right: 20px;margin-top: 50px;padding-left: 50px;padding-right: 50px;";
  } else {
    resize.style =
      "padding: 20px;margin-left: 100px;margin-right: 100px;margin-top: 50px;padding-left: 50px;padding-right: 50px;";
    resize1.style =
      "padding: 20px;margin-left: 100px;margin-right: 100px;margin-top: 50px;padding-left: 50px;padding-right: 50px;";
    resize2.style =
      "padding: 20px;margin-left: 100px;margin-right: 100px;margin-top: 50px;padding-left: 50px;padding-right: 50px;";
  }
};
console.log(window.innerWidth);
