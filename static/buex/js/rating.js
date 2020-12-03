const stars = document.querySelectorAll(".fa-star");
const messageSpan = document.querySelector(".message span");

stars.forEach((star, index) => {
  star.addEventListener("mouseover", function() {
    rate(index);
  });
});

stars.forEach((star, index) => {
  star.addEventListener("click", function() {
    messageSpan.textContent = Number(index) + 1;
    messageSpan.style.opacity = 1;
  });
});

function rate(index) {
  for (let i = 0; i < stars.length; i++) {
    if (i <= index) {
      stars[i].classList.add("gold");
    } else {
      stars[i].classList.remove("gold");
    }
  }
}

document.querySelector(".stars").addEventListener("mouseleave", reset);

function reset() {
  if (messageSpan.textContent === "") {
    stars.forEach(star => {
      star.classList.remove("gold");
    });
  } else {
    index = Number(messageSpan.textContent) - 1;
    rate(index);
  }
}
