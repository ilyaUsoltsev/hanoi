const studentId = '70256421';
let counter = 0;
const state = [];

for (let i = 0; i < studentId.length; i++) {
  const numberOfDisks = +studentId[i];
  state[i] = new Array(numberOfDisks)
    .fill(undefined)
    .map((_, idx) => numberOfDisks - idx + (8 - i) * 10);
}

function moveInState(fromRod, toRod) {
  const disk = state[fromRod].pop();
  state[toRod].push(disk);
}

function hanoi(n, fromRod, toRod, auxRod) {
  if (n === 0) {
    return;
  }
  counter++;

  // Move n-1 disks from fromRod to auxRod, using toRod as auxiliary
  hanoi(n - 1, fromRod, auxRod, toRod);
  // Move the nth disk from fromRod to toRod
  moveInState(fromRod, toRod);
  // Move the n-1 disks from auxRod to toRod, using fromRod as auxiliary
  hanoi(n - 1, auxRod, toRod, fromRod);
}

for (let i = studentId.length - 1; i > 0; i--) {
  const fromRod = i;
  const toRod = i - 1;
  const auxRod = i === studentId.length ? i - 2 : i + 1;
  hanoi(state[i].length, fromRod, toRod, auxRod);
}
console.log(state);
