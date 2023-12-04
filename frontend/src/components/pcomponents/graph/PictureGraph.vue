<template>
  <svg id="svg" width="210" height="210" xmlns="http://www.w3.org/2000/svg" @click="$emit('clickOnSVG')">
    <polygon points="100,100 100,20 180,100" class="svg-figure-color" stroke-width="2"></polygon>
    <polygon points="100,140 20,140 20,100 100,100" class="svg-figure-color" stroke-width="2"></polygon>
    <path d="M100,100 v+40 a40,40 0 0,0 40,-40z" class="svg-figure-color" stroke-width="2"></path>
    <line x1="100" y1="0" x2="100" y2="200" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="0" y1="100" x2="200" y2="100" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="97" y1="60" x2="103" y2="60" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="97" y1="20" x2="103" y2="20" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="97" y1="140" x2="103" y2="140" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="97" y1="180" x2="103" y2="180" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="60" y1="97" x2="60" y2="103" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="20" y1="97" x2="20" y2="103" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="140" y1="97" x2="140" y2="103" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="180" y1="97" x2="180" y2="103" stroke-width="2"
          class="svg-line-color"></line>
    <line x1="100" y1="0" x2="95" y2=10 stroke-width="2"
          class="svg-line-color"></line>
    <line x1="100" y1="0" x2="105" y2=10 stroke-width="2"
          class="svg-line-color"></line>
    <line x1="200" y1="100" x2="190" y2=105 stroke-width="2"
          class="svg-line-color"></line>
    <line x1="200" y1="100" x2="190" y2=95 stroke-width="2"
          class="svg-line-color"></line>
    <text x="30" y="92" class="svg-text">-R/2</text>
    <text x="6" y="92" class="svg-text">-R</text>
    <text x="107" y="30" class="svg-text">R</text>
    <text x="107" y="70" class="svg-text">R/2</text>
    <text x="110" y="10" class="svg-text">y</text>
    <text x="130" y="92" class="svg-text">R/2</text>
    <text x="170" y="92" class="svg-text">R</text>
    <text x="190" y="92" class="svg-text">x</text>
    <text x="107" y="140" class="svg-text">-R/2</text>
    <text x="107" y="180" class="svg-text">-R</text>
  </svg>
</template>

<script>
export default {
  name: "PictureGraph",
  props: ['data', 'param_r'],
  watch: {
    data() {
      this.drawAll();
    },
    param_r() {
      this.drawAll();
    }
  },
  methods: {
    drawAll() {
      this.deletePointsFromSVG();
      if (this.data.length !== 0) {
        for (let i = 0; i < this.data.length; i++) {
          let point = this.data[i];
          const x = point.x;
          const y = point.y;
          const r = point.r;
          const flagForColor = point.answer;
          let flagForR;
          if (!isNaN(x) && !isNaN(y)) {
            if (this.param_r.length > 0) {
              flagForR = (this.param_r == r);
              this.drawPoint(x, y, this.param_r, flagForColor, flagForR);
            } else {
              flagForR = (1 == r);
              this.drawPoint(x, y, 1, flagForColor, flagForR);
            }
          }
        }
      }
    },
    drawPoint(x, y, r, flagForColor, flagForR) {
      let point = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
      point.setAttribute('cx', (80 * x / r + 100).toString());
      point.setAttribute('cy', (-80 * y / r + 100).toString());
      point.setAttribute('r', (3).toString());
      point.setAttribute('data-x', x);
      point.setAttribute('data-y', y);
      if (!flagForR) point.classList.add("old-coord");
      else if (flagForColor)
        point.classList.add("good-coord");
      else point.classList.add("bad-coord");
      document.getElementById("svg").appendChild(point);
    },
    deletePointsFromSVG() {
      document.querySelectorAll(".good-coord").forEach(x => x.remove());
      document.querySelectorAll(".bad-coord").forEach(x => x.remove());
      document.querySelectorAll(".old-coord").forEach(x => x.remove());
    },
  }
}
</script>

<style>
.svg-line-color {
  stroke: rgb(104, 90, 110);
}

.svg-figure-color {
  fill: rgb(234, 234, 234);
  stroke: rgb(161, 133, 171);
}

.good-coord {
  stroke: rgb(98, 236, 151);
  fill: rgb(98, 236, 151);
}

.bad-coord {
  stroke: rgb(221, 76, 122);
  fill: rgb(221, 76, 122);
}

.old-coord {
  stroke: rgba(206, 73, 229, 0.7);
  fill: rgba(206, 73, 229, 0.7);
}

@media (max-width: 1228px) {
  .svg-text {
    font-size: 14px;
  }
}

@media (max-width: 892px) {
  .svg-text {
    font-size: 13px;
  }
}
</style>