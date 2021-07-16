function openSocketConnection() {
  const socket = new WebSocket('ws://localhost:5000/ws');
  socket.onopen = () => {
    socket.send('{"state": "connected"}')
  }

  socket.onerror = (err) => {
    console.error('Websocket error: ', err);
  }

  socket.onclose = (event) => {
    if (event.wasClean) {
      console.error(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`)
    } else {
      // e.g. server process killed or network down
      // event.code is usually 1006 in this case
      console.error(`[close] Connection closed, code=${event.code} reason=${event.reason}`)
    }
  }
  socket.onmessage = (message) => {
    // console.log('Got message from websocket:', message)
    const data = JSON.parse(message.data)
    if (data.type == 'screen') {
      handleScreenEvent(data)
    }
    if (data.type == 'slideshow') {
      handleSlideshowEvent(data)
    }
  }
}
