<template>
  <span id="welcome-message">嗨，别来无恙！</span>
</template>

<script>
import { gsap } from "gsap";

export default {
  mounted() {
    const textElement = document.getElementById("welcome-message");

    const text = textElement.innerText;
    textElement.innerHTML = text
      .split('')
      .map((char, index) => `<span class="char">${char}</span>`)
      .join('');

    const tl = gsap.timeline();

    tl.to({}, { duration: 0.6 });

    tl.fromTo(
      textElement.querySelectorAll(".char:nth-child(1), .char:nth-child(2)"),
      {
          y: 30,
          opacity: 0,
      },
      {
          y: 0,
          opacity: 1,
          duration: 0.3,
          ease: "back.out(1.7)",
          stagger: 0.15,
      }
    );

    tl.to({}, { duration: 0.4 });

    tl.fromTo(
    textElement.querySelectorAll(".char:nth-child(3), .char:nth-child(4), .char:nth-child(5), .char:nth-child(6), .char:nth-child(7)"),
      {
          y: 30,
          opacity: 0,
      },
      {
          y: 0,
          opacity: 1,
          duration: 0.3,
          ease: "back.out(1.7)",
          stagger: 0.15,
      }
    );
  },
};
</script>