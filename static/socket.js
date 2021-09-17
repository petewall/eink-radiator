/* eslint-env browser, jquery */
import { handleImageSourceEvent } from './image_source_details.js'
import { handleScreenEvent } from './screen'
import { handleSlideshowEvent } from './slideshow'

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
    console.log('Got message from websocket:', message)
    const data = JSON.parse(message.data)
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

$(document).ready(() => {
  openSocketConnection()
})
