function resize() {
    this.style.width =
        Math.max(this.value.length, this.placeholder.length) + "ch";
}

let input = document.querySelector(".status");
input.addEventListener("input", resize);
resize.call(input);
