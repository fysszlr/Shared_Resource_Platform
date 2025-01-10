<template>
  <span id="welcome-new-message">欢迎新朋友！</span>
</template>

<script>
import { gsap } from "gsap";

export default {
  mounted() {
    const textElement = document.getElementById("welcome-new-message");

    const text = textElement.innerText;
    textElement.innerHTML = text
      .split('')
      .map((char, index) => `<span class="char">${char}</span>`)
      .join('');

    gsap.fromTo(
      textElement.querySelectorAll(".char"),
      {
        opacity: 0,
      },
      {
        opacity: 1,
        duration: 0.3,
        stagger: 0.15,
      }
    );
  },
};
</script>