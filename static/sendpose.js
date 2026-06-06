

function sendPose(pose) {
    fetch("/home/send_pose", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pose: pose }),
    });
  }
  