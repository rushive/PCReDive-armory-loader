const parent = document.querySelectorAll(
  ".col-lg-12.col-md-12.col-12.mb-3 .d-flex.flex-wrap"
)[1];

const arr = [];
for (img of parent.querySelectorAll(".itemBox.col.p-2 img")) {
  arr.push(img.src);
}

const str = JSON.stringify(arr);
const res = `{ "URL": [ ${str.slice(1, -1)} ] }`;

console.log(res);
