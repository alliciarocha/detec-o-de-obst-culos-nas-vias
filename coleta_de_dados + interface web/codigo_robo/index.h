#pragma once

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Robô ESP32 + MPU6050</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Roboto', Arial, sans-serif;
      background: #EEF1F5;
      margin: 0;
      color: #333333;
      line-height: 1.6;
    }

    h1 {
      background: #1A4F7F;
      color: white;
      margin: 0;
      padding: 18px 25px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
      text-align: center;
      font-size: 2.2em;
      letter-spacing: 0.5px;
    }

    .container {
        max-width: 1200px;
        margin: 30px auto;
        padding: 0 20px;
    }

    .row {
      display: flex;
      justify-content: center;
      gap: 30px;
      flex-wrap: wrap;
      margin-bottom: 30px;
    }

    .container > .row:last-child {
        margin-bottom: 0;
    }

    .card {
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
      box-sizing: border-box;
      flex: 1 1 480px;
      transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
      min-width: 300px;
    }

    .card:hover {
      transform: translateY(-8px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.18);
    }

    h2 {
      color: #1A4F7F;
      margin-top: 0;
      margin-bottom: 20px;
      border-bottom: 2px solid #E0E4EB;
      padding-bottom: 12px;
      font-size: 1.8em;
    }

    .btn {
      display: inline-block;
      padding: 14px 28px;
      background: #3498DB;
      color: white;
      text-decoration: none;
      margin: 8px;
      border-radius: 8px;
      cursor: pointer;
      font-family: 'Roboto', sans-serif;
      font-size: 1.05em;
      font-weight: 500;
      text-align: center;
      border: none;
      transition: background 0.3s ease, transform 0.1s ease, box-shadow 0.2s ease;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .btn:hover {
      background: #2980B9;
      transform: translateY(-3px);
      box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    }
    .btn:active {
      background: #1F6B9A;
      transform: translateY(0);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .btn:focus {
      outline: none;
      box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.5);
    }

    .btn.btn-logger-start {
      background: #2ECC71;
    }
    .btn.btn-logger-start:hover {
      background: #27AE60;
    }
    .btn.btn-logger-start:active {
      background: #219150;
    }
    .btn.btn-logger-stop {
      background: #E74C3C;
    }
    .btn.btn-logger-stop:hover {
      background: #C0392B;
    }
    .btn.btn-logger-stop:active {
      background: #A03025;
    }
    .btn.download {
      background: #34495E;
    }
    .btn.download:hover {
      background: #2C3E50;
    }
    .btn.download:active {
      background: #233140;
    }

    .btn.btn-emergency-stop {
      background: #E74C3C;
      font-size: 1.2em;
      padding: 18px 36px;
      margin-top: 25px;
      display: block;
      margin-left: auto;
      margin-right: auto;
      max-width: 280px;
      border-radius: 10px;
      box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
    }
    .btn.btn-emergency-stop:hover {
      background: #C0392B;
      transform: translateY(-4px);
      box-shadow: 0 8px 20px rgba(231, 76, 60, 0.5);
    }
    .btn.btn-emergency-stop:active {
      background: #A03025;
      transform: translateY(0);
      box-shadow: 0 3px 8px rgba(231, 76, 60, 0.3);
    }
    .btn.btn-emergency-stop:focus {
      box-shadow: 0 0 0 4px rgba(231, 76, 60, 0.6);
    }

    .reading {
      font-size: 1.4em;
      margin-bottom: 10px;
      color: #555555;
      font-weight: 500;
    }

    #loggerControlCard .btn-group-primary {
      display: flex;
      justify-content: center;
      gap: 15px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }

    #loggerControlCard .btn-group-secondary {
      display: flex;
      justify-content: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    #loggerStatus {
      font-weight: bold;
      margin-top: 20px;
      font-size: 1.15em;
      text-align: center;
      padding: 10px 20px;
      border-radius: 6px;
      display: inline-block;
      min-width: 180px;
      transition: background 0.3s ease, color 0.3s ease;
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
    .logger-active {
      background: #D4EDDA;
      color: #155724;
      border: 1px solid #C3E6CB;
    }
    .logger-inactive {
      background: #F8D7DA;
      color: #721C24;
      border: 1px solid #F5C6CB;
    }

    #robotControlCard .control-grid {
      display: grid;
      grid-template-columns: repeat(3, 80px);
      gap: 20px;
      justify-content: center;
      margin-top: 25px;
    }

    .robot-control-btn {
      padding: 0;
      font-size: 2em;
      border-radius: 50%;
      width: 80px;
      height: 80px;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #5DADE2;
      color: white;
      border: none;
      cursor: pointer;
      transition: background 0.3s ease, transform 0.1s ease, box-shadow 0.2s ease;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .robot-control-btn:hover {
      background: #3498DB;
      transform: translateY(-4px);
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .robot-control-btn:active {
      background: #1F6B9A;
      transform: translateY(0);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .robot-control-btn:focus {
        outline: none;
        box-shadow: 0 0 0 4px rgba(93, 173, 226, 0.5);
    }

    @media (max-width: 768px) {
      h1 {
        font-size: 1.8em;
        padding: 15px;
      }
      .container {
        padding: 0 15px;
      }
      .row {
        flex-direction: column;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
      }
      .card {
        width: 95%;
        max-width: 400px;
        padding: 25px;
      }
      h2 {
        font-size: 1.5em;
        margin-bottom: 15px;
      }
      .btn {
        width: calc(50% - 16px);
        margin: 8px;
        padding: 12px 20px;
        font-size: 1em;
      }
      #loggerControlCard .btn-group-primary,
      #loggerControlCard .btn-group-secondary {
        justify-content: space-evenly;
        gap: 10px;
      }
      .robot-control-btn {
        width: 65px;
        height: 65px;
        font-size: 1.8em;
      }
      #robotControlCard .control-grid {
        grid-template-columns: repeat(3, 65px);
        gap: 15px;
      }
      .reading {
        font-size: 1.2em;
      }
      #loggerStatus {
        font-size: 1em;
        padding: 8px 15px;
      }
      .btn.btn-emergency-stop {
        width: calc(100% - 16px);
        max-width: none;
      }
    }

    @media (max-width: 480px) {
        .btn {
            width: calc(100% - 16px);
        }
        #loggerControlCard .btn-group-primary,
        #loggerControlCard .btn-group-secondary {
            flex-direction: column;
            align-items: center;
        }
        #robotControlCard .control-grid {
            grid-template-columns: repeat(3, 55px);
            gap: 10px;
        }
        .robot-control-btn {
            width: 55px;
            height: 55px;
            font-size: 1.6em;
        }
    }
  </style>
</head>
<body>
  <h1>Robô ESP32 + MPU6050</h1>
  <div class="container">
    <div class="row">
      <div class="card" id="gyroCard">
        <h2>Giroscópio</h2>
        <p class="reading">X: <span id="gyroX">0</span> °/s</p>
        <p class="reading">Y: <span id="gyroY">0</span> °/s</p>
        <p class="reading">Z: <span id="gyroZ">0</span> °/s</p>
      </div>

      <div class="card" id="accelerometerCard">
        <h2>Acelerômetro</h2>
        <p class="reading">X: <span id="accX">0</span> m/s²</p>
        <p class="reading">Y: <span id="accY">0</span> m/s²</p>
        <p class="reading">Z: <span id="accZ">0</span> m/s²</p>
      </div>
    </div>

    <div class="row">
      <div class="card" id="loggerControlCard">
        <h2>Logger</h2>
        <div class="btn-group-primary">
          <button class="btn btn-logger-start" onclick="startLogger()">Iniciar Logger</button>
          <button class="btn btn-logger-stop" onclick="stopLogger()">Parar Logger</button>
        </div>
        <div class="btn-group-secondary">
          <a href="/datalog" class="btn download" download="datalog.txt">Baixar Datalog</a>
        </div>
        <p id="loggerStatus" class="logger-inactive">Logger está desligado</p>
      </div>

      <div class="card" id="robotControlCard">
        <h2>Controles do Robô</h2>
        <div class="control-grid">
          <div></div>
          <button class="robot-control-btn" onmousedown="move('/f')" onmouseup="stop()">↑</button>
          <div></div>
          <button class="robot-control-btn" onmousedown="move('/l')" onmouseup="stop()">←</button>
          <button class="robot-control-btn" onmousedown="move('/b')" onmouseup="stop()">↓</button>
          <button class="robot-control-btn" onmousedown="move('/r')" onmouseup="stop()">→</button>
        </div>
        <button class="btn btn-emergency-stop" onclick="emergencyStop()">PARAR TUDO</button>
      </div>
    </div>
  </div>

<script>
  if (!!window.EventSource) {
    const source = new EventSource('/events');
    source.addEventListener('sensor_readings', function(e) {
      const data = JSON.parse(e.data);
      document.getElementById("accX").textContent = data.accX;
      document.getElementById("accY").textContent = data.accY;
      document.getElementById("accZ").textContent = data.accZ;
      document.getElementById("gyroX").textContent = data.gyroX;
      document.getElementById("gyroY").textContent = data.gyroY;
      document.getElementById("gyroZ").textContent = data.gyroZ;
    }, false);
  }

  let lastCommand = "";

  const commandMap = {
    'w': '/f',
    'arrowup': '/f',
    's': '/b',
    'arrowdown': '/b',
    'a': '/l',
    'arrowleft': '/l',
    'd': '/r',
    'arrowright': '/r'
  };

  document.addEventListener('keydown', function(event) {
    const key = event.key.toLowerCase();
    if (commandMap[key] && lastCommand !== key) {
      fetch(commandMap[key]);
      lastCommand = key;
    }
  });

  document.addEventListener('keyup', function(event) {
    const key = event.key.toLowerCase();
    if (commandMap[key]) {
      fetch("/s");
      lastCommand = "";
    }
  });

  function startLogger() {
    fetch("/startlog").then(() => {
      const statusElement = document.getElementById("loggerStatus");
      statusElement.textContent = "Logger está ativo";
      statusElement.classList.remove("logger-inactive");
      statusElement.classList.add("logger-active");
    });
  }

  function stopLogger() {
    fetch("/stoplog").then(() => {
      const statusElement = document.getElementById("loggerStatus");
      statusElement.textContent = "Logger está desligado";
      statusElement.classList.remove("logger-active");
      statusElement.classList.add("logger-inactive");
    });
  }

  function move(dir) {
    fetch(dir);
  }

  function stop() {
    fetch("/s");
  }

  function emergencyStop() {
    stop();
    stopLogger();
    console.log("Comando de emergência executado: Robô parado e Logger desligado.");
  }

  document.addEventListener('DOMContentLoaded', () => {
    const statusElement = document.getElementById("loggerStatus");
    statusElement.textContent = "Logger está desligado";
    statusElement.classList.add("logger-inactive");
  });
</script>
</body>
</html>
)rawliteral";