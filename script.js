const SIZE = 20;
const board = document.getElementById("board");
const scoreEl = document.getElementById("score");
const restartBtn = document.getElementById("restart");
const speedInput = document.getElementById("speed");

let cells = [];
let snake = [];
let dir = { x: 1, y: 0 };
let nextDir = { x: 1, y: 0 };
let food = null;
let score = 0;
let timer = null;
let paused = false;

function idx(x, y) {
  return y * SIZE + x;
}

function setCell(x, y, className, on) {
  const cell = cells[idx(x, y)];
  if (!cell) return;
  if (on) cell.classList.add(className);
  else cell.classList.remove(className);
}

function buildBoard() {
  board.innerHTML = "";
  cells = [];
  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const div = document.createElement("div");
      div.className = `cell ${(x + y) % 2 === 0 ? "a" : "b"}`;
      board.appendChild(div);
      cells.push(div);
    }
  }
}

function resetGame() {
  snake = [
    { x: Math.floor(SIZE / 2), y: Math.floor(SIZE / 2) },
    { x: Math.floor(SIZE / 2) - 1, y: Math.floor(SIZE / 2) },
  ];
  dir = { x: 1, y: 0 };
  nextDir = { x: 1, y: 0 };
  score = 0;
  scoreEl.textContent = String(score);
  food = spawnFood();
  paused = false;
  render();
}

function spawnFood() {
  let pos;
  do {
    pos = { x: Math.floor(Math.random() * SIZE), y: Math.floor(Math.random() * SIZE) };
  } while (snake.some((s) => s.x === pos.x && s.y === pos.y));
  return pos;
}

function step() {
  if (paused) return;

  dir = nextDir;
  const head = snake[0];
  const newHead = { x: head.x + dir.x, y: head.y + dir.y };

  if (newHead.x < 0 || newHead.x >= SIZE || newHead.y < 0 || newHead.y >= SIZE) {
    return gameOver();
  }
  if (snake.some((s) => s.x === newHead.x && s.y === newHead.y)) {
    return gameOver();
  }

  snake.unshift(newHead);

  if (newHead.x === food.x && newHead.y === food.y) {
    score += 1;
    scoreEl.textContent = String(score);
    food = spawnFood();
  } else {
    snake.pop();
  }

  render();
}

function render() {
  cells.forEach((c) => {
    c.classList.remove("snake", "head", "food");
  });

  setCell(food.x, food.y, "food", true);

  snake.forEach((seg, i) => {
    setCell(seg.x, seg.y, "snake", true);
    if (i === 0) setCell(seg.x, seg.y, "head", true);
  });
}

function gameOver() {
  paused = true;
}

function setSpeed() {
  const speed = Number(speedInput.value);
  if (timer) clearInterval(timer);
  timer = setInterval(step, speed);
}

function setDirection(x, y) {
  if (dir.x === -x && dir.y === -y) return; // no reverse
  nextDir = { x, y };
}

window.addEventListener("keydown", (e) => {
  const k = e.key.toLowerCase();
  if (k === "arrowup" || k === "w") setDirection(0, -1);
  else if (k === "arrowdown" || k === "s") setDirection(0, 1);
  else if (k === "arrowleft" || k === "a") setDirection(-1, 0);
  else if (k === "arrowright" || k === "d") setDirection(1, 0);
  else if (k === " ") paused = !paused;
  else if (k === "r") resetGame();
});

restartBtn.addEventListener("click", resetGame);

buildBoard();
resetGame();
setSpeed();

speedInput.addEventListener("input", setSpeed);
