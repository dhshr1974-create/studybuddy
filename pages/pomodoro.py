import streamlit as st
import streamlit.components.v1 as components

def show():
    st.title("⏱️ Pomodoro Timer")
    st.markdown("Stay focused with the proven **25-min work / 5-min break** technique.")

    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
  body { background: transparent; display: flex; flex-direction: column; align-items: center; padding: 20px; }
  .controls { display: flex; gap: 24px; margin-bottom: 24px; }
  .ctrl-box { display: flex; flex-direction: column; align-items: center; gap: 6px; }
  .ctrl-label { font-size: 13px; color: #888; }
  .ctrl-row { display: flex; align-items: center; gap: 10px; }
  .ctrl-btn { width: 32px; height: 32px; border-radius: 50%; border: none; background: #667eea; color: white; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
  .ctrl-val { font-size: 22px; font-weight: 700; color: #333; min-width: 36px; text-align: center; }
  .label { font-size: 18px; color: #666; margin-bottom: 8px; }
  .timer { font-size: 88px; font-weight: 800; color: #667eea; letter-spacing: 4px; margin: 10px 0; font-variant-numeric: tabular-nums; }
  .dots { font-size: 28px; margin: 8px 0 20px; letter-spacing: 6px; }
  .btn-row { display: flex; gap: 16px; margin-top: 8px; }
  .btn { padding: 14px 36px; font-size: 16px; font-weight: 700; border: none; border-radius: 50px; cursor: pointer; transition: transform 0.1s, opacity 0.1s; }
  .btn:active { transform: scale(0.96); opacity: 0.85; }
  .btn-start  { background: #667eea; color: white; }
  .btn-pause  { background: #f39c12; color: white; }
  .btn-reset  { background: #e74c3c; color: white; }
  .tip { margin-top: 28px; background: #f8f9fa; border-left: 4px solid #667eea; border-radius: 0 8px 8px 0; padding: 14px 18px; font-size: 13px; color: #555; line-height: 1.7; max-width: 480px; width: 100%; }
</style>
</head>
<body>

<div class="controls">
  <div class="ctrl-box">
    <div class="ctrl-label">Work (mins)</div>
    <div class="ctrl-row">
      <button class="ctrl-btn" onclick="adjust('work',-1)">−</button>
      <div class="ctrl-val" id="workVal">25</div>
      <button class="ctrl-btn" onclick="adjust('work',1)">+</button>
    </div>
  </div>
  <div class="ctrl-box">
    <div class="ctrl-label">Break (mins)</div>
    <div class="ctrl-row">
      <button class="ctrl-btn" onclick="adjust('break',-1)">−</button>
      <div class="ctrl-val" id="breakVal">5</div>
      <button class="ctrl-btn" onclick="adjust('break',1)">+</button>
    </div>
  </div>
  <div class="ctrl-box">
    <div class="ctrl-label">Sessions</div>
    <div class="ctrl-row">
      <button class="ctrl-btn" onclick="adjust('sess',-1)">−</button>
      <div class="ctrl-val" id="sessVal">4</div>
      <button class="ctrl-btn" onclick="adjust('sess',1)">+</button>
    </div>
  </div>
</div>

<div class="label" id="timerLabel">🍅 Work Session 1</div>
<div class="timer" id="timerDisplay">25:00</div>
<div class="dots" id="dotDisplay"></div>

<div class="btn-row">
  <button class="btn btn-start" onclick="startTimer()">▶ Start</button>
  <button class="btn btn-pause" onclick="pauseTimer()">⏸ Pause</button>
  <button class="btn btn-reset" onclick="resetTimer()">↺ Reset</button>
</div>

<div class="tip">
  💡 <strong>Tips:</strong> Phone away during work sessions &nbsp;|&nbsp; 
  Stand up during breaks &nbsp;|&nbsp; 
  After 4 sessions take a 15–30 min longer break
</div>

<script>
  let workMins  = 25, breakMins = 5, totalSess = 4;
  let remaining = workMins * 60;
  let isWork    = true, running = false, sessCount = 0;
  let interval  = null;

  function adjust(type, delta) {
    if (running) return;
    if (type === 'work')  { workMins  = Math.max(1, Math.min(60, workMins  + delta)); document.getElementById('workVal').innerText  = workMins;  }
    if (type === 'break') { breakMins = Math.max(1, Math.min(30, breakMins + delta)); document.getElementById('breakVal').innerText = breakMins; }
    if (type === 'sess')  { totalSess = Math.max(1, Math.min(10, totalSess + delta)); document.getElementById('sessVal').innerText  = totalSess; }
    remaining = workMins * 60;
    updateDisplay();
  }

  function fmt(s) {
    return String(Math.floor(s/60)).padStart(2,'0') + ':' + String(s%60).padStart(2,'0');
  }

  function updateDisplay() {
    document.getElementById('timerDisplay').innerText = fmt(remaining);
    document.getElementById('timerLabel').innerText   = isWork ? '🍅 Work Session ' + (sessCount+1) + ' / ' + totalSess : '☕ Break Time!';
    document.getElementById('timerDisplay').style.color = isWork ? '#667eea' : '#27ae60';
    let dots = '';
    for (let i = 0; i < totalSess; i++) dots += i < sessCount ? '🍅' : '⭕';
    document.getElementById('dotDisplay').innerText = dots;
  }

  function startTimer() {
    if (running) return;
    running = true;
    interval = setInterval(() => {
      remaining--;
      updateDisplay();
      if (remaining <= 0) {
        clearInterval(interval); running = false;
        if (isWork) {
          sessCount++;
          if (sessCount >= totalSess) {
            document.getElementById('timerLabel').innerText = '🏆 All done! Great work!';
            document.getElementById('timerDisplay').innerText = '00:00';
            return;
          }
          isWork = false; remaining = breakMins * 60;
        } else {
          isWork = true; remaining = workMins * 60;
        }
        updateDisplay();
        startTimer();
      }
    }, 1000);
  }

  function pauseTimer() { clearInterval(interval); running = false; }

  function resetTimer() {
    clearInterval(interval); running = false;
    isWork = true; sessCount = 0;
    remaining = workMins * 60;
    updateDisplay();
  }

  updateDisplay();
</script>
</body>
</html>
""", height=520)
