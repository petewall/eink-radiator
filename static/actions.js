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

let refreshPreviewImage = () => refreshImage('/preview-image.png', previewImage)
let refreshRadiatorImage = async () => {
    radiatorImage.classList.add('loading')
    setImageButton.setAttribute('disabled', 'disabled')
    await refreshImage('/radiator-image.png', radiatorImage)
    setImageButton.removeAttribute('disabled')
}

const imageSources = document.getElementById("image_sources")
imageSources.onchange = async (e) => {
    previewImage.classList.add('loading')
    await fetch(`/select_source/${e.target.selectedIndex}`, {
        method: 'POST'
    })
    await getConfiguration()
    await refreshPreviewImage()
}

const configurationContainer = document.getElementById('configuration')
const saveConfigButton = document.getElementById('saveConfig')

function removeConfiguration() {
    saveConfigButton.setAttribute('disabled', 'disabled')
    while (configurationContainer.firstChild) {
        configurationContainer.removeChild(configurationContainer.lastChild);
    }
}

function makeTextField(name, value, isPassword) {
    let field = document.createElement('input')
    field.setAttribute('name', name)
    if (isPassword) {
        field.setAttribute('type', 'password')
    }
    field.value = value
    return field
}

function makeSelection(name, value, options) {
    let dropdown = document.createElement('select')
    dropdown.setAttribute('name', name)
    for (let option of options) {
        let option_obj = document.createElement('option')
        option_obj.setAttribute('value', option)
        option_obj.innerText = option
        dropdown.appendChild(option_obj)
    }
    dropdown.value = value
    return dropdown
}

function makeTextArea(name, value) {
    let field = document.createElement('textarea')
    field.setAttribute('name', name)
    field.value = value
    return field
}

async function getConfiguration() {
    removeConfiguration()

    let response = await fetch('/source')
    let configuration = await response.json()
    for (let key in configuration) {
        let label = document.createElement('label')
        label.setAttribute('for', key)
        label.innerText = `${key}: `
        configurationContainer.appendChild(label)

        if (configuration[key] == null || typeof configuration[key] === 'string') {
            configurationContainer.appendChild(makeTextField(key, configuration[key], key === 'password'))
        } else if (configuration[key].type === 'select') {
            configurationContainer.appendChild(makeSelection(key, configuration[key].value, configuration[key].options))
        } else if (configuration[key].type === 'textarea') {
            configurationContainer.appendChild(makeTextArea(key, configuration[key].value))
        }
    }
    saveConfigButton.removeAttribute('disabled')
}

saveConfigButton.onclick = async () => {
    let config = {}
    for (let node of configurationContainer.childNodes) {
        if (node.tagName === 'INPUT' ||
            node.tagName === 'SELECT' ||
            node.tagName === 'TEXTAREA') {
            config[node.getAttribute('name')] = node.value
        }
    }

    previewImage.classList.add('loading')
    await fetch('/source', {
        method: 'PATCH',
        body: JSON.stringify(config),
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        }
    })
    await refreshPreviewImage()
}

setImageButton.onclick = async () => {
    setImageButton.setAttribute('disabled', 'disabled')
    radiatorImage.classList.add('loading')

    await fetch('/set_image', {
        method: 'POST'
    })

    await refreshRadiatorImage()
    setImageButton.removeAttribute('disabled')
}

refreshPreviewImage()
refreshRadiatorImage()
getConfiguration()
