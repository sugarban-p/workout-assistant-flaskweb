// DOMContentLoaded -- 當網頁的 DOM 結構完全加載後，執行這段程式碼
document.addEventListener("DOMContentLoaded", init);
var first = false;

function init() {
  const toggleButton = document.getElementById("toggle-button");
  const cameraContainer = document.getElementById("camera-container");
  const textContainer = document.getElementById("text-container");
  let cameraOn = false;
  toggleButton.addEventListener("click", function () {
    if (!cameraOn) {
      startCamera(toggleButton, cameraContainer);
      cameraOn = true;
    } else {
      stopCamera(toggleButton, cameraContainer, textContainer);
      cameraOn = false;
    }
  });
}

function startCamera(toggleButton, cameraContainer) {
  toggleButton.textContent = "結束";
  if (!first) {
    cameraContainer.innerHTML = `<div style="display: flex; justify-content: center; align-items: center; height: 100%; color: white; font-size: 60px; font-weight: bolder">正在取得解析度...</div>`;
    first = true;
  }
  fetch("/home/start")
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        cameraContainer.innerHTML = `<img src="/home/video_feed?timestamp=${new Date()
          .getTime()
          .toString()
          .slice(-2)}&random=${Math.floor(
          Math.random() * 1000
        )}" alt="Camera Feed" id="camera-feed">`;
      }
    })
    .catch((error) => console.error("Error starting camera:", error));
}

function stopCamera(toggleButton, cameraContainer, textContainer) {
  fetch("/home/stop")
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        toggleButton.textContent = "開啟";
        cameraContainer.innerHTML = "";
        textContainer.textContent = `計時: ${data.time} 秒\n${data.systemlog}`;
      }
    })
    .catch((error) => console.error("Error stopping camera:", error));
}
