"use strict";
function changeImage() {
  requestAnimationFrame(changeImage);

  var url = document.getElementById("img-1").src;

  if (url == "Images/apples.jfif") {
    document.getElementById("img-1").src = "Resources/Share2.bmp";
  } else {
    if (url == "Resources/Share2.bmp") {
      document.getElementById("img-1").src = "Resources/Share1.bmp";
    }
  }
}
