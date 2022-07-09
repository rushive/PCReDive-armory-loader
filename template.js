const json = ``;

const obj = JSON.parse(json);
const itemList = JSON.parse(localStorage.getItem("itemList"));

const ret = itemList.map((item) => {
  const id = item["equipment_id"];
  if (!obj[id]) return item;
  return { ...item, count: Number(obj[id].slice(1)) };
});

localStorage.setItem("itemList", JSON.stringify(ret));
