const timer = document.getElementById("question-timer");

if (timer) {
  const bonusMessage = document.getElementById("timer-bonus");
  const bonusSeconds = Number(timer.dataset.bonusSeconds) || 10;
  let elapsed = Number(timer.dataset.elapsed) || 0;
  let lastTick = performance.now();

  const updateTimer = () => {
    const now = performance.now();
    elapsed += (now - lastTick) / 1000;
    lastTick = now;
    timer.textContent = `${elapsed.toFixed(1)} seconds`;
    const bonusExpired = elapsed > bonusSeconds;
    timer.classList.toggle("bonus-expired", bonusExpired);
    bonusMessage.textContent = bonusExpired
      ? "Speed bonus no longer available"
      : "Speed bonus available";
  };

  updateTimer();
  window.setInterval(updateTimer, 100);
}
