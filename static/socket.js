/* eslint-env browser, jquery */
/* global handleImageSourceEvent, handleScreenEvent, handleSlideshowEvent */

function openSocketConnection() {
  const host = $(location).attr('host')
  const socket = new WebSocket(`ws://${host}/ws`);
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
    const data = JSON.parse(message.data)
    console.log('Got message from websocket:', data)
    if (data.type == 'image_source') {
      handleImageSourceEvent(data)
    }
    if (data.type == 'screen') {
      handleScreenEvent(data)
    }
    if (data.type == 'slideshow') {
      handleSlideshowEvent(data)
    }
  }
}

$(() => {
  openSocketConnection()
})
