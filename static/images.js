/*eslint no-unused-vars: "off"*/

function bufferToBase64(buffer) {
  let binary = '';
  let bytes = [].slice.call(new Uint8Array(buffer))
  bytes.forEach((b) => binary += String.fromCharCode(b))
  return window.btoa(binary)
}

async function refreshImage(url, image) {
  let response = await fetch(url)
  if (response.status === 200) {
      let buffer = await response.arrayBuffer()
      image.style.backgroundImage = `url("data:image/png;base64,${bufferToBase64(buffer)}")`
  } else {
      image.style.backgroundImage = ""
  }
  image.classList.remove('loading')
}

const previewImage = document.getElementById('preview-image')
const radiatorImage = document.getElementById('radiator-image')
const setImageButton = document.getElementById('setImage')

setImageButton.onclick = async () => {
  setImageButton.setAttribute('disabled', 'disabled')
  radiatorImage.classList.add('loading')

  await fetch('/set_image', {
      method: 'POST'
  })

  await refreshRadiatorImage()
  setImageButton.removeAttribute('disabled')
}

const refreshPreviewImage = () => refreshImage('/preview-image.png', previewImage)
const refreshRadiatorImage = async () => {
    radiatorImage.classList.add('loading')
    setImageButton.setAttribute('disabled', 'disabled')
    await refreshImage('/radiator-image.png', radiatorImage)
    setImageButton.removeAttribute('disabled')
}
