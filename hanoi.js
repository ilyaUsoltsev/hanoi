const state = [
  [85, 84, 83, 82, 81],
  [75, 74, 73, 72, 71],
  [65, 64, 63, 62, 61],
  [55, 54, 53, 52, 51],
  [45, 44, 43, 42, 41],
  [35, 34, 33, 32, 31],
  [23, 22],
  [13, 12, 11],
];

function moveInState(fromRod, toRod) {
  console.log('move in state', fromRod, toRod);
  const disk = state[fromRod].pop();
  state[toRod].push(disk);
  console.log(state);
}

function hanoi(n, source, auxiliary, target) {
  // Base case: When there's only one disc, just move it to the target peg.
  if (n === 0) {
    return;
  }

  // Recursive case: move the smaller stack (n-1 discs) to the auxiliary peg.
  hanoi(n - 1, source, target, auxiliary);

  // Move the nth disc to the target peg.
  moveInState(source, target);

  // Move the smaller stack from auxiliary peg to target peg.
  hanoi(n - 1, auxiliary, source, target);
}

function pushToRight(from, to, n) {
  let counter = n;
  while (counter > 0) {
    moveInState(from, to);
    counter--;
  }
}

for (let i = state.length - 2; i >= 0; i--) {
  if (i === 0) {
    pushToRight(0, 2, state[i].length);
    let hanoiShift = 5;
    let start = 2;
    while (hanoiShift > 0) {
      console.log('11', start);

      hanoi(state[start].length, start, start - 1, start + 1);
      start++;
      hanoiShift--;
    }
  } else {
    pushToRight(i, i + 1, state[i].length);
    let hanoiShift = state.length - i - 2;
    let start = i + 1;
    while (hanoiShift > 0) {
      console.log('22');
      hanoi(state[start].length, start, start - 1, start + 1);
      start++;
      hanoiShift--;
    }
  }
}
console.log('------');
console.log(state);
